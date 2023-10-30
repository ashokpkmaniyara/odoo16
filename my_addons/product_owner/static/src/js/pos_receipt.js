odoo.define('product_owner.models', function(require) {
    'use strict';

    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrderline = (Orderline) => class CustomOrderline extends Orderline {
        export_for_printing() {
            var result = super.export_for_printing();
            if (this.get_product().owner_id){
            result['owner_id'] = this.get_product().owner_id[1];}
            return result;
        }
    }
    Registries.Model.extend(Orderline, CustomOrderline);
});