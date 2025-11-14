// DOM이 완전히 로드된 후 실행
document.addEventListener('DOMContentLoaded', function() {
    let rowIndex = 0; // 행 인덱스 추적

        // 기본값 설정 함수 (재사용 가능)
        function setDefaultValues(inputs, isNewRow = false) {
            inputs.forEach((input, index) => {
                if (input.type === 'radio') {
                    // 새 행인 경우 라디오 버튼 name 변경 (각 행마다 독립적인 그룹)
                    if (isNewRow) {
                        const radioGroup = `is_promotion_${rowIndex}`;
                        input.name = radioGroup;
                    }
                    // 기본값: 비프로모션(0) 선택
                    if (input.value === '0') {
                        input.checked = true;
                    } else {
                        input.checked = false;
                    }
                } else if (input.type === 'number') {
                // 숫자 입력 필드에 기본값 설정
                const fieldName = input.name;
                
                switch(fieldName) {
                    case 'month':
                        input.value = '1';
                        break;
                    case 'tv_ad_spend':
                        input.value = '100';
                        break;
                    case 'online_ad_spend':
                        input.value = '50';
                        break;
                    case 'price_index':
                        input.value = '1.0';
                        break;
                    case 'holiday_cnt':
                        input.value = '0';
                        break;
                    case 'competitor_index':
                        input.value = '1.0';
                        break;
                    default:
                        input.value = '';
                }
            }
        });
    }

    function addRow() {
        // 더 명확한 선택자 사용
        const tbody = document.querySelector('#form table tbody');
        
        if (!tbody) {
            console.error('tbody를 찾을 수 없습니다.');
            return;
        }
        
        const firstRow = tbody.querySelector('tr');
        
        if (!firstRow) {
            console.error('첫 번째 행을 찾을 수 없습니다.');
            return;
        }
        
        const newRow = firstRow.cloneNode(true);
        
        // 행 인덱스 증가
        rowIndex++;
        
        // 모든 입력 필드 가져오기
        const inputs = newRow.querySelectorAll('input');
        
        // 기본값 설정 (새 행이므로 isNewRow = true)
        setDefaultValues(inputs, true);
        
        // 새 행을 테이블에 추가
        tbody.appendChild(newRow);
    }

    // 페이지 로드 시 첫 번째 행에 기본값 설정
    function initializeFirstRow() {
        const tbody = document.querySelector('#form table tbody');
        if (!tbody) {
            return;
        }
        
        const firstRow = tbody.querySelector('tr');
        if (!firstRow) {
            return;
        }
        
        const inputs = firstRow.querySelectorAll('input');
        setDefaultValues(inputs, false); // 첫 번째 행이므로 name 변경 안 함
    }

    // 첫 번째 행 초기화
    initializeFirstRow();

    // 버튼 클릭 이벤트 리스너
    const addRowButton = document.getElementById('add_row');
    if (addRowButton) {
        addRowButton.addEventListener('click', addRow);
    } else {
        console.error('입력 행 추가 버튼을 찾을 수 없습니다.');
    }
});

