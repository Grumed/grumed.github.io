# Text-only GitHub Pages Blog (KOR)

아주 가벼운 **흑백 · 텍스트 전용** 블로그 템플릿입니다.  
Markdown을 작성하고 `build.py`를 실행하면 HTML, index, sitemap, RSS, robots.txt가 생성됩니다.

## 사용법 (로컬)

1) Python 설치 후:
```bash
pip install markdown
```
2) 설정 편집: `config.py`에서 `SITE_TITLE`, `AUTHOR`, `BASE_URL` 값을 바꾸세요.  
   - GitHub Pages 주소 예: `https://yourname.github.io`
   - 커스텀 도메인 사용 시 해당 주소로 설정

3) 글 작성
```
posts_src/
  2025-10-05-hello.md
```
- 1행: 제목(마크다운 헤딩 가능 `# 제목`)
- 2행: 날짜(YYYY-MM-DD)
- 3행 이후: 본문

4) 빌드
```bash
python build.py
```
- `posts/*.html`, `index.html`, `sitemap.xml`, `rss.xml`, `robots.txt` 생성

5) GitHub Pages 배포
- GitHub에서 `yourname.github.io` 이름의 public 저장소 생성
- 이 폴더 전체를 push
- 저장소 → **Settings → Pages** → `Deploy from branch` 활성화
- 잠시 후 `https://yourname.github.io` 접속

## 폴더 구조
```
.
├─ build.py          # 빌더 스크립트
├─ config.py         # 사이트 설정
├─ index.html        # (빌드 시 생성/갱신)
├─ sitemap.xml       # (빌드 시 생성)
├─ rss.xml           # (빌드 시 생성)
├─ robots.txt        # (빌드 시 생성)
├─ posts/            # HTML 결과물
└─ posts_src/        # Markdown 원문
```

## 자주 묻는 질문
- **이미지 넣기?**  
  `images/` 폴더를 만들고 `<img src="images/xxx.webp" alt="">`처럼 사용하세요.
- **티스토리/네이버 대비 장점?**  
  초경량, 완전한 커스터마이즈, 코드/버전관리, 무료 호스팅.
- **Google 검색 노출?**  
  `sitemap.xml`, `robots.txt` 생성되며, Search Console 등록 권장.

행운을 빕니다!
