def migrate(cr, version):
    """
    Migracja z Selection na Char dla parametrów szafek
    """
    if not version:
        return
    
    # Usuń stare definicje pól z ir.model.fields
    cr.execute("""
        DELETE FROM ir_model_fields 
        WHERE model = 'product.template' 
        AND name IN ('parametr_nogi', 'parametr_uchyt', 'parametr_drzwi')
        AND ttype = 'selection'
    """)
    
    # Usuń stare selection values
    cr.execute("""
        DELETE FROM ir_model_fields_selection 
        WHERE field_id IN (
            SELECT id FROM ir_model_fields 
            WHERE model = 'product.template' 
            AND name IN ('parametr_nogi', 'parametr_uchyt', 'parametr_drzwi')
        )
    """)
