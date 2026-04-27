# 📋 LFSQ 대시보드 GitHub Pages 배포 가이드

팀원 모두가 같은 링크로 최신 대시보드를 볼 수 있게 배포하는 방법입니다.

---

## 📁 파일 구성

```
lfsq-dashboard/
├── index.html    ← 대시보드 본체
├── data.json     ← 현재 매출 데이터 (매달 갱신)
├── convert.py    ← 엑셀 → data.json 변환 스크립트
└── README.md     ← 이 가이드
```

---

## 🚀 1단계 — GitHub 계정 만들기 (처음 1회)

1. **https://github.com** 접속 → [Sign up] 클릭
2. 이메일, 비밀번호, 사용자명 입력 후 가입
3. 이메일 인증 완료

---

## 📦 2단계 — 저장소(Repository) 만들기 (처음 1회)

1. GitHub 로그인 후 오른쪽 상단 **[+] → New repository** 클릭
2. Repository name: `lfsq-dashboard` 입력
3. **Public** 선택 (GitHub Pages 무료 사용을 위해)
4. **[Create repository]** 클릭

---

## ⬆️ 3단계 — 파일 업로드 (처음 1회)

1. 방금 만든 저장소 페이지에서 **[uploading an existing file]** 클릭
2. 아래 3개 파일을 드래그해서 업로드:
   - `index.html`
   - `data.json`
   - `convert.py`
3. 하단 **[Commit changes]** 클릭

---

## 🌐 4단계 — GitHub Pages 활성화 (처음 1회)

1. 저장소 상단 탭 **[Settings]** 클릭
2. 왼쪽 메뉴 **[Pages]** 클릭
3. Source 아래 Branch를 **main** 으로 변경 → **[Save]**
4. 잠시 후 페이지 상단에 링크 생성:

```
https://[내 GitHub 계정명].github.io/lfsq-dashboard/
```

이 링크를 팀원들에게 공유하면 됩니다! ✅

---

## 🔄 매달 데이터 업데이트 방법

### 방법 A — Python 스크립트 사용 (권장)

```bash
# 터미널에서 실행
pip install pandas openpyxl
python convert.py 온오프데이터_작업용_SAP_test.xlsx
```
→ `data.json` 파일이 자동 생성됩니다.

### 방법 B — 직접 업로드

1. GitHub 저장소 접속
2. `data.json` 파일 클릭
3. 연필(✏️) 아이콘 클릭 → 내용 수정 or 파일 아이콘 클릭 → 새 파일로 업로드
4. **[Commit changes]** 클릭

업로드 후 1~2분 내에 링크에 반영됩니다.

---

## 💡 대시보드 바로 보기 (파일 없이)

링크 접속 시 오른쪽 상단 **[📂 엑셀 파일 업로드]** 버튼을 통해
엑셀 파일을 직접 드래그하면 `data.json` 없이도 바로 데이터를 확인할 수 있습니다.

---

## ❓ 자주 묻는 질문

**Q. 링크가 팀 외부에 공개되나요?**
A. Public 저장소는 URL을 아는 사람은 누구나 볼 수 있습니다.
   비공개로 하려면 저장소를 Private으로 설정하고 GitHub Pro(유료)를 사용해야 합니다.
   또는 Netlify(무료)를 사용하면 비밀번호 보호 기능이 있습니다.

**Q. 데이터 업데이트 후 언제 반영되나요?**
A. GitHub에 파일을 올린 후 보통 1~3분 내에 반영됩니다.

**Q. 엑셀 시트 구조가 바뀌면 어떻게 하나요?**
A. `convert.py` 파일의 행 번호(예: `v(df26, 13, 2)`)를 수정해야 합니다.
   필요하면 Claude에게 새 파일을 첨부하고 업데이트 요청하세요.
