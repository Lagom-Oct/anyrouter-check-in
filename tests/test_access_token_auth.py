from types import SimpleNamespace

import checkin
from utils.config import AccountConfig, AppConfig, load_accounts_config


def test_load_accounts_accepts_access_token(monkeypatch):
	monkeypatch.setenv(
		'ANYROUTER_ACCOUNTS',
		'[{"name":"AgentRouter","provider":"agentrouter","access_token":"secret-token","api_user":"197424"}]',
	)

	accounts = load_accounts_config()

	assert accounts is not None
	assert len(accounts) == 1
	assert accounts[0].has_access_token()
	assert accounts[0].provider == 'agentrouter'
	assert accounts[0].api_user == '197424'


def test_access_token_requires_api_user(monkeypatch):
	monkeypatch.setenv(
		'ANYROUTER_ACCOUNTS',
		'[{"provider":"agentrouter","access_token":"secret-token"}]',
	)

	assert load_accounts_config() is None


def test_run_check_in_requests_sends_bearer_token_and_user_header(monkeypatch):
	request_headers = []

	class FakeCookies:
		def update(self, cookies):
			assert cookies == {'acw_tc': 'waf-cookie'}

	class FakeClient:
		def __init__(self, **kwargs):
			self.cookies = FakeCookies()

		def __enter__(self):
			return self

		def __exit__(self, exc_type, exc, traceback):
			return False

		def get(self, url, headers, timeout):
			request_headers.append(headers.copy())
			return SimpleNamespace(
				status_code=200,
				json=lambda: {
					'success': True,
					'data': {'quota': 500000, 'used_quota': 0},
				},
			)

	monkeypatch.setattr(checkin.httpx, 'Client', FakeClient)

	account = AccountConfig(
		cookies=None,
		api_user='197424',
		provider='agentrouter',
		access_token='secret-token',
	)
	provider = SimpleNamespace(
		domain='https://agentrouter.org',
		user_info_path='/api/user/self',
		api_user_key='new-api-user',
		needs_manual_check_in=lambda: False,
	)

	success, before, after = checkin.run_check_in_requests(
		{'acw_tc': 'waf-cookie'},
		account,
		'AgentRouter',
		provider,
	)

	assert success is True
	assert before and before['success'] is True
	assert after and after['success'] is True
	assert request_headers
	assert all(headers['Authorization'] == 'Bearer secret-token' for headers in request_headers)
	assert all(headers['new-api-user'] == '197424' for headers in request_headers)


def test_build_access_token_headers():
	account = AccountConfig(
		cookies=None,
		api_user='197424',
		provider='agentrouter',
		access_token='secret-token',
	)
	provider = SimpleNamespace(api_user_key='new-api-user')

	headers = checkin.build_access_token_headers(account, provider)

	assert headers['Authorization'] == 'Bearer secret-token'
	assert headers['new-api-user'] == '197424'


async def test_check_in_account_uses_browser_for_access_token(monkeypatch):
	account = AccountConfig(
		cookies=None,
		api_user='197424',
		provider='agentrouter',
		name='AgentRouter',
		access_token='secret-token',
	)
	provider = SimpleNamespace(domain='https://agentrouter.org')
	app_config = AppConfig(providers={'agentrouter': provider})
	expected = (True, {'success': True}, {'success': True})
	called = {}

	async def fake_browser_check_in(received_account, account_name, received_provider):
		called['account'] = received_account
		called['name'] = account_name
		called['provider'] = received_provider
		return expected

	monkeypatch.setattr(checkin, 'run_access_token_check_in_with_browser', fake_browser_check_in)

	result = await checkin.check_in_account(account, 0, app_config)

	assert result == expected
	assert called == {'account': account, 'name': 'AgentRouter', 'provider': provider}
