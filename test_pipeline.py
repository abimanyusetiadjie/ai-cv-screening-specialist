import glob
import json
import os
from pipeline import run_batch_screening

def test_full_pipeline():
    with open('job_presets.json', 'r', encoding='utf-8') as f:
        presets = json.load(f)

    preset = presets['plant_cad_drafter']
    jd = preset['job_description']
    criteria = preset['criteria']

    files = sorted(glob.glob('sample_cvs/*.pdf'))
    print(f'Testing automated screening on {len(files)} CVs...')
    print(f'Target Position : {preset["job_title"]}')
    print(f'Criteria        : {criteria}')
    print('-' * 70)

    df, errors = run_batch_screening(files, jd, criteria)

    assert not df.empty, 'DataFrame cannot be empty'
    print(f'Total processed: {len(df)}')

    print('\n=== HASIL RANKING KANDIDAT ===')
    cols = ['Nama', 'Email', 'No. Telepon', 'Lolos Syarat Wajib', 'Skor Embedding', 'Skor LLM', 'Skor Akhir']
    print(df[cols].to_string(index=True))

    print('\n=== AUDIT DETAIL KANDIDAT ===')
    for idx, row in df.iterrows():
        print(f'Rank #{idx} - {row["Nama"]} (Skor: {row["Skor Akhir"]})')
        print(f'  Lolos Syarat Wajib : {row["Lolos Syarat Wajib"]}')
        print(f'  Kekuatan           : {row["Kekuatan"]}')
        print(f'  Kekurangan         : {row["Kekurangan"]}')
        print(f'  Reasoning          : {row["Alasan"]}')
        print('-' * 70)

    if errors:
        print(f'Peringatan: {len(errors)} error: {errors}')
    else:
        print('Semua 5 CV berhasil diproses 100% tanpa error!')

if __name__ == '__main__':
    test_full_pipeline()
