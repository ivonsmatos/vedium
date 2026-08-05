import glob

scripts = glob.glob('vedium_core/vedium_core/scripts/migrations/oneshot/seed_ingls_*_catalog.py')
for script in scripts:
    with open(script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir a variável incorreta
    if '"enabled": 1 if stripe_price_id else 0,' in content:
        content = content.replace('"enabled": 1 if stripe_price_id else 0,', '"enabled": 1 if p_data.get("price_id") else 0,')
        with open(script, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed {script}')
