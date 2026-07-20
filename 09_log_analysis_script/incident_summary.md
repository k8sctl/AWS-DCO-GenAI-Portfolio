# 📋 DCO 교육용 샘플 로그 분석 보고서

이 보고서는 파이썬 스크립트(`analyze_logs.py`)에 의해 자동으로 생성된 교육용 DCO 분석 문서입니다.

## 1. 전체 요약 (Overview)
- **전체 분석된 로그 줄 수**: 140개

## 2. 심각도(Severity)별 개수 집계
| 심각도(Severity) | 발생 건수 | 비율 |
| :--- | :---: | :---: |
| `ERROR` | 2건 | 1.4% |
| `INFO` | 135건 | 96.4% |
| `WARNING` | 3건 | 2.1% |

## 3. 이벤트(Event) 종류별 발생 횟수
| 이벤트 이름(Event) | 발생 횟수 |
| :--- | :---: |
| Normal heartbeat | 125회 |
| Ticket opened | 3회 |
| Ticket escalated | 3회 |
| Maintenance completed | 3회 |
| Fan Alert | 1회 |
| Temperature warning | 1회 |
| SSD failure warning | 1회 |
| CRC error 증가 | 1회 |
| Link Down | 1회 |
| Link Up | 1회 |

## 4. 경고(WARNING) 및 심각(CRITICAL / ERROR) 로그 세부 목록
| 발생 시간 | 대상 장비 | 심각도 | 이벤트 종류 | 상세 로그 메시지 |
| :--- | :--- | :---: | :--- | :--- |
| 2026-07-03 01:05:00 | `DEMO_CORE_SW_02` | **WARNING** | Fan Alert | Fan module 2 RPM dropped to 15% (Below threshold 20%). IP: 198.51.100.2 |
| 2026-07-03 02:05:00 | `EDU_SRV_R04_N12` | **WARNING** | Temperature warning | Chassis temperature reached 42C (Threshold: 40C). IP: 192.0.2.12 |
| 2026-07-03 02:10:00 | `EDU_SRV_R04_N12` | **ERROR** | SSD failure warning | Drive Slot 3 SSD wearout indicator FAILING (SMART wear 96%). IP: 192.0.2.12 |
| 2026-07-03 03:05:00 | `SAMPLE_TOR_SW_01` | **WARNING** | CRC error 증가 | Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1 |
| 2026-07-03 03:06:00 | `SAMPLE_TOR_SW_01` | **ERROR** | Link Down | Interface Gi0/1 status changed to DOWN. Connection to server lost. |

## 5. 주요 인프라 장애 및 처리 상태 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
현업 DCO 장비 관리 및 케이블링, 티켓 처리 과정에서 정기 모니터링해야 하는 주요 항목 상태 요약입니다.

### 🔍 CRC_ERROR (네트워크 전송/물리적 레이어 오류)
네트워크 장비의 포트/케이블 전송 오류가 발생한 내역입니다.

- **시간**: `2026-07-03 03:05:00` | **장비**: `SAMPLE_TOR_SW_01`
  - **상세**: CRC error 증가 - *"Interface Gi0/1 CRC error counter increased to 154 within 5 minutes. IP: 192.0.2.1"*
- **시간**: `2026-07-03 03:30:00` | **장비**: `SAMPLE_TOR_SW_01`
  - **상세**: Normal heartbeat - *"System status is healthy. Interface Gi0/1 running with 0 CRC errors. IP: 192.0.2.1"*

### 🔌 LINK_DOWN (장비 물리적 포트 연결 끊김)
네트워크 또는 서버의 인터페이스가 비활성화(DOWN)되어 연결이 차단된 기록입니다.

- **시간**: `2026-07-03 03:06:00` | **장비**: `SAMPLE_TOR_SW_01`
  - **상세**: Link Down - *"Interface Gi0/1 status changed to DOWN. Connection to server lost."*

### 🚨 TICKET_ESCALATED (장애 대응 팀 지정 및 에스컬레이션)
장애가 자동으로 해결되지 않거나 부품 교체가 필요하여 담당 실무 그룹으로 티켓이 이관(Escalation)된 상황입니다.

- **시간**: `2026-07-03 01:10:00` | **장비**: `DEMO_CORE_SW_02`
  - **상세**: Ticket escalated - *"Ticket EDU-TKT-2026-0001 escalated to Local Infrastructure Team."*
- **시간**: `2026-07-03 02:15:00` | **장비**: `EDU_SRV_R04_N12`
  - **상세**: Ticket escalated - *"Ticket EDU-TKT-2026-0002 escalated to DCO Hardware Support."*
- **시간**: `2026-07-03 03:12:00` | **장비**: `SAMPLE_TOR_SW_01`
  - **상세**: Ticket escalated - *"Ticket EDU-TKT-2026-0003 escalated to Onsite Cabling Team."*

