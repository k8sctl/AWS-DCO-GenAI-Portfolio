import os

def analyze_dco_logs(input_filename="sample_dco_log.txt", output_filename="incident_summary.md"):
    # 1. 입력 파일 존재 여부 확인
    if not os.path.exists(input_filename):
        print(f"[오류] '{input_filename}' 파일을 찾을 수 없습니다.")
        print("현재 폴더에 'sample_dco_log.txt' 파일이 존재하는지 확인해 주세요.")
        return False

    # 2. 통계 및 요약을 위한 변수(데이터 저장소) 준비
    total_lines = 0                   # 전체 로그 라인 수
    severity_counts = {}              # 심각도(Severity)별 개수 예: {"INFO": 10, "ERROR": 2}
    event_counts = {}                 # 이벤트(Event) 이름별 개수 예: {"Normal heartbeat": 5}
    warning_critical_logs = []        # WARNING 이나 CRITICAL 상태의 로그들만 따로 저장할 리스트
    
    # 주요 관심 이벤트들을 담기 위한 딕셔너리
    # CRC 에러, 링크 다운, 티켓 에스컬레이션 이벤트를 추적합니다.
    major_events = {
        "CRC_ERROR": [],
        "LINK_DOWN": [],
        "TICKET_ESCALATED": []
    }

    # 3. 로그 파일 열고 한 줄씩 읽어서 분석하기
    print(f"'{input_filename}' 분석을 시작합니다...")
    
    # 'with open'을 사용하면 파일을 다 읽은 후 자동으로 안전하게 닫아줍니다.
    # 한국어(UTF-8) 인코딩으로 파일을 읽습니다.
    with open(input_filename, "r", encoding="utf-8") as file:
        for line in file:
            # 줄 끝에 들어있는 줄바꿈 문자('\n') 등을 깨끗이 지웁니다.
            line = line.strip()
            
            # 만약 빈 줄(공백)이 있다면 분석하지 않고 건너뜁니다.
            if not line:
                continue
                
            total_lines += 1
            
            # 로그의 형식은 파이프 기호('|')로 나뉘어 있습니다.
            # 예: YYYY-MM-DD HH:MM:SS | DEVICE | SEVERITY | EVENT | MESSAGE
            # split('|')을 통해 각 요소를 리스트로 나눕니다.
            parts = [part.strip() for part in line.split("|")]
            
            # 정상적인 로그 형식(5개 이상의 필드)인지 확인합니다.
            if len(parts) >= 5:
                timestamp = parts[0]  # 날짜와 시간 (예: 2026-07-03 00:00:00)
                device = parts[1]     # 장비명 (예: SAMPLE_TOR_SW_01)
                severity = parts[2]   # 심각도 (예: INFO, WARNING, ERROR)
                event = parts[3]      # 이벤트 종류 (예: Normal heartbeat, Link Down)
                message = parts[4]    # 구체적 세부 내용 (예: System status is healthy...)
            else:
                # 파이프로 분할되지 않는 비정상적인 행은 분석에서 제외합니다.
                continue

            # (1) 심각도(Severity)별 개수 카운팅
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # (2) 이벤트(Event)별 개수 카운팅
            event_counts[event] = event_counts.get(event, 0) + 1

            # (3) WARNING 또는 CRITICAL 로그 수집 (ERROR도 심각한 상황이므로 함께 포함하면 좋습니다)
            if severity.upper() in ["WARNING", "CRITICAL", "ERROR"]:
                warning_critical_logs.append({
                    "timestamp": timestamp,
                    "device": device,
                    "severity": severity,
                    "event": event,
                    "message": message
                })

            # (4) 특정 중요 키워드 분류 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
            event_upper = event.upper()
            message_upper = message.upper()

            # A. CRC_ERROR 체크 (CRC 에러 증가 등)
            if "CRC" in event_upper or "CRC" in message_upper:
                major_events["CRC_ERROR"].append({
                    "timestamp": timestamp,
                    "device": device,
                    "event": event,
                    "message": message
                })

            # B. LINK_DOWN 체크 (링크 다운 등)
            if "LINK DOWN" in event_upper or "LINK_DOWN" in event_upper or "LINK DOWN" in message_upper:
                major_events["LINK_DOWN"].append({
                    "timestamp": timestamp,
                    "device": device,
                    "event": event,
                    "message": message
                })

            # C. TICKET_ESCALATED 체크 (티켓 에스컬레이션 / 이관 등)
            if "ESCALATED" in event_upper or "ESCALATED" in message_upper or "TICKET ESCALATED" in event_upper:
                major_events["TICKET_ESCALATED"].append({
                    "timestamp": timestamp,
                    "device": device,
                    "event": event,
                    "message": message
                })

    # 4. 분석된 결과를 Markdown(마크다운) 형식의 파일로 저장하기
    print(f"분석 결과를 보고서 파일('{output_filename}')로 저장하는 중입니다...")
    
    with open(output_filename, "w", encoding="utf-8") as out:
        out.write("# 📋 DCO 교육용 샘플 로그 분석 보고서\n\n")
        out.write("이 보고서는 파이썬 스크립트(`analyze_logs.py`)에 의해 자동으로 생성된 교육용 DCO 분석 문서입니다.\n\n")
        
        # 4-1. 전체 요약
        out.write("## 1. 전체 요약 (Overview)\n")
        out.write(f"- **전체 분석된 로그 줄 수**: {total_lines}개\n\n")
        
        # 4-2. 심각도별 개수 (표 형식)
        out.write("## 2. 심각도(Severity)별 개수 집계\n")
        out.write("| 심각도(Severity) | 발생 건수 | 비율 |\n")
        out.write("| :--- | :---: | :---: |\n")
        for sev, count in sorted(severity_counts.items()):
            percentage = (count / total_lines) * 100 if total_lines > 0 else 0
            out.write(f"| `{sev}` | {count}건 | {percentage:.1f}% |\n")
        out.write("\n")
        
        # 4-3. 이벤트별 개수 (표 형식, 발생 빈도가 많은 순으로 정렬)
        out.write("## 3. 이벤트(Event) 종류별 발생 횟수\n")
        out.write("| 이벤트 이름(Event) | 발생 횟수 |\n")
        out.write("| :--- | :---: |\n")
        sorted_events = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
        for evt, count in sorted_events:
            out.write(f"| {evt} | {count}회 |\n")
        out.write("\n")
        
        # 4-4. WARNING 및 CRITICAL / ERROR 로그 목록
        out.write("## 4. 경고(WARNING) 및 심각(CRITICAL / ERROR) 로그 세부 목록\n")
        if warning_critical_logs:
            out.write("| 발생 시간 | 대상 장비 | 심각도 | 이벤트 종류 | 상세 로그 메시지 |\n")
            out.write("| :--- | :--- | :---: | :--- | :--- |\n")
            for log in warning_critical_logs:
                out.write(f"| {log['timestamp']} | `{log['device']}` | **{log['severity']}** | {log['event']} | {log['message']} |\n")
        else:
            out.write("*현재 로그 파일에서 경고나 오류성 로그가 감지되지 않았습니다.*\n")
        out.write("\n")
        
        # 4-5. 핵심 관심 이벤트 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)
        out.write("## 5. 주요 인프라 장애 및 처리 상태 요약 (CRC_ERROR, LINK_DOWN, TICKET_ESCALATED)\n")
        out.write("현업 DCO 장비 관리 및 케이블링, 티켓 처리 과정에서 정기 모니터링해야 하는 주요 항목 상태 요약입니다.\n\n")
        
        # CRC_ERROR 요약
        out.write("### 🔍 CRC_ERROR (네트워크 전송/물리적 레이어 오류)\n")
        if major_events["CRC_ERROR"]:
            out.write("네트워크 장비의 포트/케이블 전송 오류가 발생한 내역입니다.\n\n")
            for item in major_events["CRC_ERROR"]:
                out.write(f"- **시간**: `{item['timestamp']}` | **장비**: `{item['device']}`\n")
                out.write(f"  - **상세**: {item['event']} - *\"{item['message']}\"*\n")
        else:
            out.write("✅ CRC_ERROR 관련 이벤트가 감지되지 않았습니다.\n")
        out.write("\n")
        
        # LINK_DOWN 요약
        out.write("### 🔌 LINK_DOWN (장비 물리적 포트 연결 끊김)\n")
        if major_events["LINK_DOWN"]:
            out.write("네트워크 또는 서버의 인터페이스가 비활성화(DOWN)되어 연결이 차단된 기록입니다.\n\n")
            for item in major_events["LINK_DOWN"]:
                out.write(f"- **시간**: `{item['timestamp']}` | **장비**: `{item['device']}`\n")
                out.write(f"  - **상세**: {item['event']} - *\"{item['message']}\"*\n")
        else:
            out.write("✅ LINK_DOWN 관련 이벤트가 감지되지 않았습니다.\n")
        out.write("\n")
        
        # TICKET_ESCALATED 요약
        out.write("### 🚨 TICKET_ESCALATED (장애 대응 팀 지정 및 에스컬레이션)\n")
        if major_events["TICKET_ESCALATED"]:
            out.write("장애가 자동으로 해결되지 않거나 부품 교체가 필요하여 담당 실무 그룹으로 티켓이 이관(Escalation)된 상황입니다.\n\n")
            for item in major_events["TICKET_ESCALATED"]:
                out.write(f"- **시간**: `{item['timestamp']}` | **장비**: `{item['device']}`\n")
                out.write(f"  - **상세**: {item['event']} - *\"{item['message']}\"*\n")
        else:
            out.write("✅ TICKET_ESCALATED 관련 상태 이관 이벤드가 감지되지 않았습니다.\n")
        out.write("\n")

    print(f"성공! 분석 보고서가 '{output_filename}' 파일로 작성 완료되었습니다.")
    return True

if __name__ == "__main__":
    analyze_dco_logs()