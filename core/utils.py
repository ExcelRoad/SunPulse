
def generate_unique_number(prefix: str, model_class, field_name: str = 'number') -> str:
    '''
    create a unique number with a prefix for each record type
    example: CUS-0001, CUS-0002, SYS-0001
    '''
    last_obj = models_class.objects.filter(
        **{f'{field_name}__startswith': f'{prefix}-'}
    ).order_by(f'-{field_name}').first()

    if last_obj:
        last_number = int(getattr(last_obj, field_name).split('-')[-1])
        new_number = last_number + 1
    else:
        new_number = 1
    
    return f'{prefix}-{new_number:06d}'

