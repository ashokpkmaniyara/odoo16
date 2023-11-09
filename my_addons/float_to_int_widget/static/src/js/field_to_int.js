/** @odoo-module**/
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
const { Component,useRef } = owl

class FloatToInt extends Component{
    setup(){
        super.setup();
        this.input = useRef('inputNumber')
    }
    _onSelectNumber(ev) {
        var num = ev.target.value;
        var roundValue = Math.round(num);
        this.input.el.value = roundValue;
        this.props.update(roundValue);
    }
}
FloatToInt.template = "float_to_int_widget.FloatToInt";
registry.category("fields").add("float_to_int", FloatToInt);