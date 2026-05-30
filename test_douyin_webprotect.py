#!/usr/bin/env python3
"""
使用完整的 Cookie + webProtect 测试抖音解析
"""
import sys
import os
import requests
import json
import re
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2'))

print("=" * 60)
print("使用完整配置测试抖音解析")
print("=" * 60)

# 你提供的完整数据
cookie_str = "hevc_supported=true; bd_ticket_guard_client_web_domain=2; live_use_vvc=%22false%22; SEARCH_RESULT_LIST_TYPE=%22multi%22; SearchMultiColumnLandingAbVer=2; enter_pc_once=1; __druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0EyOTglMkMlMjJjbGllbnRIZWlnaHQlMjIlM0E0NzAlMkMlMjJ3aWR0aCUyMiUzQTI5OCUyQyUyMmhlaWdodCUyMiUzQTQ3MCUyQyUyMmRldmljZVBpeGVsUmF0aW8lMjIlM0ExLjI1JTJDJTIydXNlckFnZW50JTIyJTNBJTIyTW96aWxsYSUyRjUuMCUyMChXaW5kb3dzJTIwTlQlMjAxMC4wJTNCJTIwV2luNjQlM0IlMjB4NjQpJTIwQXBwbGVXZWJLaXQlMkY1MzcuMzYlMjAoS0hUTUwlMkMlMjBsaWtlJTIwR2Vja28pJTIwQ2hyb21lJTJGMTM4LjAuMC4wJTIwU2FmYXJpJTJGNTM3LjM2JTIwRWRnJTJGMTM4LjAuMC4wJTIyJTdE; xgplayer_user_id=55744895773; UIFID_TEMP=22328dfa2c6129151bd9a70c452335694b5e7d73b1c813963f5ad42d97dbea2b70a5cffb70219f368b5781c05c07a44e98e3a4c96b72aade237c6e515ba50b3dba7da740df30247d61df9eb0fc3b90; fpk1=U2FsdGVkX1+w9Jwav0nObUVQPqvsAqTicxQhXqOE8COTL5SL/1tXsUKhFp0PCFNXsLMTjbYfoTrBtjS0bGp00A==; fpk2=7ceed19ee5ebdbf792f56329591ffc53; UIFID=22328dfa2c6129151bd9a70c452335694b5e7d73b1c813963f5ad42d97dbea2b70a5cffb70219f368b5781c05c07a44e98e3a4c96b72aade237c6e515ba50b3dba7da740df30247d61df9eb0fc3b90; theme=%22dark%22; manual_theme=%22dark%22; enter_pc_first_on_day=20251216; xgplayer_device_id=14674103620; __live_version__=%221.1.4.6396%22; passport_assist_user=Cjy_oDxG87tm_1BwcF_yw_8QjPrAKI6WIexh3oNW3B-yEfG1MEWtwboHxx0MOpJOIoDG75R7prrlYw7VcqoaSgo8AAAAAAAAAAAAAFADHYNBIgQciNtnJoHCFX3lS3hgbsi1zIGZbsOPwQVGzScg0FbSIdbGn0t_TnvHSK_7EOKmiA4Yia_WVCABIgEDmd0BcA%3D%3D; n_mh=dvLn-j_FUamR48o_U5dGpuRUbHGScpTW_aXHiESPdvM; uid_tt=1ef37b3164f503eafafadd790a96fe2c; uid_tt_ss=1ef37b3164f503eafafadd790a96fe2c; sid_tt=689800b77e6c750aae06533651b3cbe3; sessionid=689800b77e6c750aae06533651b3cbe3; sessionid_ss=689800b77e6c750aae06533651b3cbe3; is_staff_user=false; login_time=1769776746845; _bd_ticket_crypt_cookie=f416ba1dac5f2a029ca582e1c473ddb8; has_biz_token=false; dy_swidth=1920; dy_sheight=1080; is_dash_user=1; my_rd=2; s_v_web_id=verify_move9dsk_5niJR7ha_VSnd_4SFs_81N5_9L8APr042fcJ; passport_csrf_token=2347d2cd985614892d274e8d9bf15cfa; passport_csrf_token_default=2347d2cd985614892d274e8d9bf15cfa; __security_mc_1_s_sdk_crypt_sdk=60db123d-4c4f-b970; __security_mc_1_s_sdk_cert_key=e86dc32d-4334-88c4; __security_mc_1_s_sdk_sign_data_key_web_protect=332bfa0e-40aa-bf98; PhoneResumeUidCacheV1=%7B%2299905995153%22%3A%7B%22time%22%3A1779857786328%2C%22blockingTime%22%3A1780116991480%2C%22noClick%22%3A0%7D%7D; =douyin.com; xg_device_score=7.343081279409702; device_web_cpu_core=16; device_web_memory_size=32; architecture=amd64; is_support_rtm_web_ts=1; strategyABtestKey=%221780034424.11%22; ttwid=1%7CbwIoVhstVO52aAr7xb8eAon_5lhIW6FwQGcM2RgzhJ0%7C1780034425%7C5ad4690226efa5b2d538dcc67d212779e9b6573f01363cbb5cd6cebd4a951494; sid_guard=689800b77e6c750aae06533651b3cbe3%7C1780034430%7C5184000%7CTue%2C+28-Jul-2026+06%3A00%3A30+GMT; session_tlb_tag=sttt%7C5%7CdJgAt35sdQquBlM2UbPL4__________AEHgSn_IKtJE_j_wj-niKRWKOWipUf68jt3KJClq4oRY%3D; sid_ucp_v1=1.0.0-KDQ2ZWEzNDE0YjdhMzY3ZTk4ZDE4YzRiOTlhYTQwYTgzZTE4Y2I1YjIKHwiUg_KW9AIQ_tbk0AYY7zEgDDC_o-jYBTgFQPsHSAQaAmhsIiA2ODk4MDBiNzdlNmM3NTBhYWUwNjUzMzY1MWIzY2JlMw; ssid_ucp_v1=1.0.0-KDQ2ZWEzNDE0YjdhMzY3ZTk4ZDE4YzRiOTlhYTQwYTgzZTE4Y2I1YjIKHwiUg_KW9AIQ_tbk0AYY7zEgDDC_o-jYBTgFQPsHSAQaAmhsIiA2ODk4MDBiNzdlNmM3NTBhYWUwNjUzMzY1MWIzY2JlMw; SelfTabRedDotControl=%5B%7B%22id%22%3A%227493830959305852965%22%2C%22u%22%3A60%2C%22c%22%3A0%7D%2C%7B%22id%22%3A%227493560514685962290%22%2C%22u%22%3A71%2C%22c%22%3A0%7D%5D; volume_info=%7B%22isMute%22%3Afalse%2C%22isUserMute%22%3Afalse%2C%22volume%22%3A0.5%7D; __ac_signature=_02B4Z6wo00f01qboZZgAAIDCKKUTrx1-k.KmyGEAAMOvc2; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A32%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAALGSUlyBtanX0ZsWJ3OXOl2c7yfOAzkpFwzvWk2-RRLs%2F1780070400000%2F0%2F0%2F1780061237552%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAALGSUlyBtanX0ZsWJ3OXOl2c7yfOAzkpFwzvWk2-RRLs%2F1780070400000%2F0%2F0%2F1780061837553%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTVpkQmE0bEswMnFhUFFPRjkyZG55UklSdUk4ZmVwakdNWmlNdklDbU5NazBZekRRenJISFhzTVFobjd3cmZmUGwzc2pSQ1VvOThXRzBjYzhMMHVhdmc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=8a2a8dfd143b329f610e400644db24adbb1480dde417fab4d11d6b2fae4b218df93b4e67ff14910b4557f6906ea33bc5c13f9e3dcff5138a0204f2f0e97ae73f7c67eabd92cf2777c5e102b95e593a4f; biz_trace_id=a5fe85e9; publish_badge_show_info=%221%2C0%2C0%2C1780060642409%22; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f2771777060272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e5927666d776a686028607d71606b766c6a6b3f2a2a6a61756d6b676d6c61616d61756a6666676c64696969606f64646f6068616c6a2a7666776c7571762a6c6b76756066716a772b6f76592758272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f27636469766027292771273f27343c36323631363335353d3234272927676c715a75776a716a666a69273f2763646976602778; bit_env=dpjjQ1eEPGPTImlaoColZh68ynN5ft6D5wJ6cLMvOo0jqS1fsSF6G5oPN-1OueDc7-FlJPEM0AmxcaxAIDLPbly3SFp07PGlaxXKV5ZI7FY0j5jisuyT35pk0VNi3oQvaoyitgGAsNe9TucAcDYx4gPC3atK4ZQAnKjQ13jAN4YUi6xEhnuXp_LewenQBydoc3b65XNVaPIXNpAA4azsDgaF6q-uI27otA3yhLFRw8zHEiMxAVHTHxAWMkBJARJpTTfz0Ei7CL4JqUzFRZLxjlro94GN-GdQsqDhCTymHIi3HERscXZiam7rEY0zrw54zB6Decv7R_e93tOmyWpyUkc8mqxqixB_14BP4LoFXiIPaFaqeI6_WB4deNo12cgygFjmzLUCMM-LWKfkxhBU8JaVdFkWjTtvJM6e5prma_ta1GGqI4H6s2YBdwD_XDEYC6AFA_G_yuACfcZ4WPalras13lKfXpSAhYJ6EsbX45uWjxLeJ6yEWbeXCuQ16rKvmFmyUqEKz9lNVQ_gwAeCyhmRkC85B5p76lSM2NkWHrE%3D; gulu_source_res=eyJwX2luIjoiMDM5NTkxYTlhNTA5ZWZjZTcyNGNiODBkODlkYjA1MzhiZWI3MTY2MGUxYTI2YWRiY2Q4MjNlYjY3M2Y5NmZjNCJ9; passport_auth_mix_state=y1s620yai6y5xhbvzjceuamv0l8507c4; bd_ticket_guard_client_data_v2=eyJyZWVfcHVibGljX2tleSI6IkJNWmRCYTRsSzAycWFQUU9GOTJkbnlSSVJ1SThmZXBqR01aaU12SUNtTk1rMFl6RFF6ckhIWHNNUWhuN3dyZmZQbDNzalJDVW85OFdHMGNjOEwwdWF2Zz0iLCJ0c19zaWduIjoidGguMS40NGIxZDFmM2QxNDg2ZWM5OWMxNTE2MjU0Y2ExYTJlOTExODgwNTljMGUwYjcxZjMwNjlmM2NlOWY4YjJmMWNlYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcF9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiJjb3dMNVBoVzRZekpuWEdzbFVMZmIxblFaRjNQSGIyRk04MmtiRUtXWmpVPSIsInNlY19zcyI6IiNlYjRqQUFWNUIwczNSYXRDSy

webprotect_data = json.loads('{"ticket":"689800b77e6c750aae06533651b3cbe3","ts_sign":"ts.1.44b1d1f3d1486ec99c1516254ca1a2e91188059c0e0b71f3069f3ce9f8b2f1cec4fbe87d2319cf05318624ceda14911ca406dedbebeddb2e30fce8d4fa02575d","client_cert":"pub.BMZdBa4lK02qaPQOF92dnyRIRuI8fepjGMZiMvICmNMk0YzDQzrHHXsMQhn7wrffPl3sjRCUo98WG0cc8L0uavg=","log_id":"20260130203906C115E392C6568894B7DF","create_time":1769776746}')

print(f"\n[1] 测试1: 不使用 webprotect")
print(f"    只使用 Cookie")

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.douyin.com/',
    'Cookie': cookie_str,
}

# 获取视频ID
video_id = "7636490241968311592"
api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}"

params = {
    'aid': '6383',
    'count': '1',
    'version_name': '5.1.2',
    'version_code': '50102',
    'device_platform': 'webapp',
    'os': 'windows',
    'SSMix': '1',
    'improvement_sincerely_thread': '1',
    'share_douyin': '1',
}

try:
    resp1 = requests.get(api_url, headers=headers1, params=params, timeout=15)
    print(f"    状态码: {resp1.status_code}")
    data1 = resp1.json()
    print(f"    响应: {json.dumps(data1, ensure_ascii=False)[:500]}")
except Exception as e:
    print(f"    [FAIL] {e}")

print(f"\n[2] 测试2: 添加 webprotect 相关头")
print(f"    需要在请求头中添加 X-Token 或类似字段")

# webprotect 数据中的 ticket 可能用作某个头
headers2 = headers1.copy()
# 尝试添加一些可能的头
headers2['X-Token'] = webprotect_data.get('ticket', '')
headers2['X-Ts-Sign'] = webprotect_data.get('ts_sign', '')

try:
    resp2 = requests.get(api_url, headers=headers2, params=params, timeout=15)
    print(f"    状态码: {resp2.status_code}")
    data2 = resp2.json()
    print(f"    响应: {json.dumps(data2, ensure_ascii=False)[:500]}")
except Exception as e:
    print(f"    [FAIL] {e}")

print("\n" + "=" * 60)
print("说明：")
print("1. 抖音的 Cookie 模式需要正确的签名（X-Bogus 或 X-Token）")
print("2. 这个签名通常是 JS 生成的，不能直接从 Cookie 中获取")
print("3. 可能需要使用 TikHub API 或者找到签名生成算法")
print("=" * 60)
