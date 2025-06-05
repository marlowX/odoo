from odoo import models, fields, api

class StockReorderRule(models.Model):
    _inherit = 'stock.warehouse.orderpoint'
    
    # Połącz z naszymi parametrami magazynowymi
    @api.model
    def create_reorder_rules_from_product(self, product_id):
        """Tworzy reguły uzupełniania na podstawie parametrów produktu"""
        product = self.env['product.template'].browse(product_id)
        if product.reorder_point and product.min_stock_level:
            vals = {
                'product_id': product.product_variant_id.id,
                'product_min_qty': product.min_stock_level,
                'product_max_qty': product.max_stock_level or product.min_stock_level * 2,
                'qty_multiple': 1,
                'warehouse_id': self.env['stock.warehouse'].search([], limit=1).id,
            }
            return self.create(vals)
        return False

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def create_reorder_rule(self):
        """Przycisk do tworzenia reguły uzupełniania"""
        reorder_rule = self.env['stock.warehouse.orderpoint']
        return reorder_rule.create_reorder_rules_from_product(self.id)
