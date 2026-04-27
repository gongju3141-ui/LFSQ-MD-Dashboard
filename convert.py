"""
LFSQ 대시보드 데이터 변환 스크립트
사용법: python convert.py 엑셀파일명.xlsx
"""
import sys, json, pathlib
import pandas as pd

def v(df, r, c):
    try:
        val = df.iloc[r, c]
        return round(float(val), 2) if pd.notna(val) else 0.0
    except:
        return 0.0

def convert(xlsx_path):
    print(f"📂 파일 읽는 중: {xlsx_path}")
    df26 = pd.read_excel(xlsx_path, sheet_name='26년 실적', header=None)
    df25 = pd.read_excel(xlsx_path, sheet_name='25년 실적', header=None)

    # ── 25년 기준 데이터
    total25 = v(df25, 4, 1)
    lic25   = v(df25, 32, 1)
    ip25 = {
        'LFSQ':        v(df25, 15, 1),
        'ORIGINAL':    v(df25, 10, 1),
        'ARTIST':      v(df25, 17, 1),
        'Patnership':  v(df25, 27, 1)
    }

    # ── 26년 총매출 (row40, section2 총합계)
    total26 = v(df26, 40, 2)

    # ── IP별 총매출 (section2)
    ip_total = {
        'LFSQ':        v(df26, 13, 2),
        'ORIGINAL':    v(df26, 15, 2),
        'ARTIST':      v(df26, 23, 2),
        'Patnership':  v(df26, 34, 2)
    }

    # ── IP별 사입 매출 (section3)
    ip_lic = {
        'LFSQ':        v(df26, 48, 2),
        'ORIGINAL':    v(df26, 50, 2),
        'ARTIST':      v(df26, 55, 2),
        'Patnership':  v(df26, 58, 2)
    }
    total_lic26 = v(df26, 63, 2)

    # ── MD별 총매출
    md_total_map = {
        'LFSQ':        {'MULTI':   v(df26, 14, 2)},
        'ORIGINAL':    {'B&F':     v(df26, 16, 2), 'COLLER': v(df26, 17, 2),
                        'DHB':     v(df26, 18, 2), 'LTC':    v(df26, 19, 2),
                        'MININI':  v(df26, 20, 2), 'SSEB':   v(df26, 21, 2),
                        'ZNF':     v(df26, 22, 2)},
        'ARTIST':      {'ATZ':     v(df26, 24, 2), 'BT21':   v(df26, 25, 2),
                        'IDLE':    v(df26, 26, 2), 'NCTD':   v(df26, 27, 2),
                        'NJ':      v(df26, 28, 2), 'PLAVE':  v(df26, 29, 2),
                        'TRZ':     v(df26, 30, 2), 'ZB1':    v(df26, 31, 2)},
        'Patnership':  {'JUG':     v(df26, 35, 2), 'DT':     v(df26, 36, 2),
                        'MONA':    v(df26, 37, 2), 'PIC':    v(df26, 38, 2)}
    }

    # ── MD별 사입 매출
    md_lic_map = {
        'LFSQ':        {'MULTI':   v(df26, 49, 2)},
        'ORIGINAL':    {'B&F':     v(df26, 51, 2), 'COLLER': v(df26, 52, 2),
                        'MININI':  v(df26, 53, 2), 'ZNF':    v(df26, 54, 2)},
        'ARTIST':      {'BT21':    v(df26, 56, 2), 'ZB1':    v(df26, 57, 2)},
        'Patnership':  {'JUG':     v(df26, 59, 2), 'DT':     v(df26, 60, 2),
                        'MONA':    v(df26, 61, 2), 'PIC':    v(df26, 62, 2)}
    }

    # ── 채널별 총매출 (section6)
    ch_total = {
        '통합몰':                     v(df26, 202, 2),
        '스마트스토어':               v(df26, 203, 2),
        '카카오커머스':               v(df26, 204, 2),
        '29CM':                       v(df26, 205, 2),
        '라인프렌즈 스퀘어 명동점':   v(df26, 207, 2),
        '라인프렌즈 스퀘어 성수점':   v(df26, 208, 2),
        '분당스퀘어':                 v(df26, 209, 2),
        '인사동점':                   v(df26, 210, 2),
        '홍대점':                     v(df26, 211, 2),
    }

    # ── 채널별 사입 매출 (section7)
    ch_lic = {
        '통합몰':                     v(df26, 224, 2),
        '스마트스토어':               v(df26, 225, 2),
        '카카오커머스':               v(df26, 226, 2),
        '29CM':                       0,
        '라인프렌즈 스퀘어 명동점':   v(df26, 228, 2),
        '홍대점':                     v(df26, 229, 2),
        '라인프렌즈 스퀘어 성수점':   v(df26, 230, 2),
        '분당스퀘어':                 v(df26, 231, 2),
        '인사동점':                   v(df26, 232, 2),
    }

    # ── 브랜드: LFSQ (section4, row83~109)
    lfsq_brands = []
    for i in range(83, 110):
        nm = df26.iloc[i, 1]; rv = df26.iloc[i, 2]
        if pd.notna(nm) and pd.notna(rv) and '합계' not in str(nm):
            try: lfsq_brands.append({'n': str(nm).strip(), 'v': round(float(rv), 2)})
            except: pass

    # ── 브랜드: LC (section5, row128~174)
    lc_brands = {'ARTIST': [], 'ORIGINAL': [], 'Patnership': []}
    cur_ip = None
    for i in range(128, 175):
        nm = df26.iloc[i, 1]; rv = df26.iloc[i, 2]
        if not pd.notna(nm): continue
        s = str(nm).strip()
        if s in ['ARTIST', 'ORIGINAL', 'Patnership']:
            cur_ip = s; continue
        if '합계' in s: continue
        if cur_ip and pd.notna(rv):
            try: lc_brands[cur_ip].append({'n': s, 'v': round(float(rv), 2)})
            except: pass

    # ── MULTI vs LC
    multi_lic = ip_lic['LFSQ']
    lc_lic    = total_lic26 - multi_lic
    multi_pct = round(multi_lic / total_lic26 * 100, 1) if total_lic26 else 0
    lc_pct    = round(lc_lic / total_lic26 * 100, 1) if total_lic26 else 0

    data = {
        'meta': {'month': '26년 4월', 'prev_month': '25년 4월'},
        'kpi': {
            'total26':   total26,
            'lic26':     total_lic26,
            'total25':   total25,
            'lic25':     lic25,
            'multi_lic': multi_lic,
            'lc_lic':    round(lc_lic, 2),
            'multi_pct': multi_pct,
            'lc_pct':    lc_pct
        },
        'ip': [
            {'ip': g, 'total': ip_total[g], 'lic': ip_lic[g], 'lic25': ip25[g]}
            for g in ['LFSQ', 'ORIGINAL', 'ARTIST', 'Patnership']
        ],
        'md': [
            {'ip': ip, 'md': md,
             'total': md_total_map[ip].get(md, 0),
             'lic':   md_lic_map[ip].get(md, 0)}
            for ip in ['LFSQ', 'ORIGINAL', 'ARTIST', 'Patnership']
            for md in md_total_map[ip]
        ],
        'channels': [
            {'type': '온라인',  'ch': ch, 'total': ch_total[ch], 'lic': ch_lic.get(ch, 0)}
            for ch in ['통합몰', '스마트스토어', '카카오커머스', '29CM']
        ] + [
            {'type': '오프라인', 'ch': ch, 'total': ch_total[ch], 'lic': ch_lic.get(ch, 0)}
            for ch in ['라인프렌즈 스퀘어 명동점', '홍대점', '라인프렌즈 스퀘어 성수점', '인사동점', '분당스퀘어']
        ],
        'brands': {
            'LFSQ':       lfsq_brands,
            'ORIGINAL':   lc_brands.get('ORIGINAL', []),
            'ARTIST':     lc_brands.get('ARTIST', []),
            'Patnership': lc_brands.get('Patnership', [])
        }
    }

    out_path = pathlib.Path('.') / 'data.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ data.json 생성 완료: {out_path}")
    print(f"   총매출: {total26:,.0f}원 | 사입: {total_lic26:,.0f}원 ({total_lic26/total26*100:.1f}%)")
    print(f"   MULTI {multi_pct}% / LC {lc_pct}%")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python convert.py 파일명.xlsx")
        sys.exit(1)
    convert(sys.argv[1])
