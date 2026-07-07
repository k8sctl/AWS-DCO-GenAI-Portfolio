# [교육용 샘플 데이터 / FOR EDUCATIONAL USE ONLY]
> 본 문서는 교육용 실습을 위해 가상으로 작성된 샘플 데이터이며, 실제 인프라, 실제 장비, 실제 고객 정보와는 전혀 무관합니다.

## 교육용 샘플 장애 티켓 (EDU-TICKET-SAMPLE-001)

### 1. 기본 정보
- **티켓 ID**: EDU-TICKET-SAMPLE-001
- **발생 시간 (UTC)**: 2026-07-07 06:00:00 (샘플 시간)
- **샘플 장비명**: SAMPLE_TOR_SW_01 (EDU_MODEL_SWITCH_X)
- **이벤트명**: Interface Link Down (Preceded by CRC Error Increase)
- **심각도**: SEV-SAMPLE-2 (높음 - 교육용 레벨)
- **Escalation 필요 여부**: 필요 (YES - SAMPLE_OPS_LEVEL_2로 이관 필요)

### 2. 관찰 내용 (Scenario Observations)
- **현상**:
  1. `SAMPLE_TOR_SW_01` 스위치의 특정 교육용 샘플 포트(Port: SAMPLE-Eth1/1)에서 10분간 CRC Error가 급격하게 증가하는 현상이 먼저 관찰됨.
  2. CRC Error 증가 누적 후, 최종적으로 해당 링크가 Down 상태(`Link Down`)로 전환됨.
- **샘플 로그 요약**:
  ```
  [2026-07-07T06:00:00Z] %SAMPLE_PORT-5-ERR_DISABLE: crc error threshold exceeded on SAMPLE-Eth1/1.
  [2026-07-07T06:00:05Z] %SAMPLE_PORT-5-LINK_STATUS: SAMPLE-Eth1/1 changed state to down.
  ```

### 3. 보안 및 운영 주의사항
- **주의**:
  - 본 티켓 정보 및 대응 절차는 학습용 가상 시나리오입니다.
  - 실제 환경의 IP 주소, 장비 시리얼 번호, 실제 자격 증명(Credential), 고객 식별 정보 등은 이 문서에 절대 기록하거나 포함해서는 안 됩니다.
  - 외부 네트워크 대상을 향한 어떠한 실제 점검 명령(ping, traceroute 등)도 제안하거나 실행해서는 안 됩니다.
