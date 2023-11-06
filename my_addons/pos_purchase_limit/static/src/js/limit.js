odoo.define('pos_purchase_limit.models', function (require) {
"use strict";

const Registries = require('point_of_sale.Registries');
const ProductScreen = require('point_of_sale.ProductScreen');

const PurchaseLimit = (ProductScreen) => class PurchaseLimit extends ProductScreen{
    async _onClickPay() {
          if (this.currentOrder.get_partner()){
                var order_amount = this.currentOrder.get_total_with_tax()
                if (order_amount>this.currentOrder.get_partner().limit && this.currentOrder.get_partner().purchase_limit){
                    this.showPopup('ErrorPopup', {
                    title: this.env._t('Limit exceeded'),
                    body: this.env._t('Purchase limit for the customer is exceeded'),
                });
                }else{
                    return super._onClickPay();
                }
          }else{
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Customer needed'),
                    body: this.env._t('Customer is required to do the payment'),
                });
           }
    }
}
    Registries.Component.extend(ProductScreen, PurchaseLimit);
});
