import React from 'react';
import { useSelector } from "react-redux";


const FiveConcept: React.FC = () => {

    // THIS CODE IS ADDED FOR 5X5 CONCEPT
const currentClientState = useSelector((state) => state);
function callSize() {
    // debugger;
    const { annotation: { canvas: { instance: { model: { data: { activeElement:{clientID,...frr}, ...rr }, ...or }, ...oor }, ...rest }, ...onrest }, ...ononrest } = currentClientState;
    // console.log(activeElement);


    const {annotation:{job:{labels,...rd},...rrr},...rrrr} = currentClientState;
    var new_arr = [];
    labels.map(item =>{return new_arr.push(item.name)})
    console.log(new_arr)
    var dd = document.getElementById(`cvat_canvas_shape_${clientID}`);
    // var dd = document.getElementById("cvat_canvas_shape_1");
    var dheight = Math.round(parseFloat(dd.instance.height()))
    var dwidth = Math.round(parseFloat(dd.instance.width()))
    var node_id = dd.parentElement.instance._defs.node.id;
    var new_el_id = parseInt(node_id.substr(9)) - 1
    var df = document.getElementById(`SvgjsDefs${new_el_id}`)
    var html_val = df.nextElementSibling.children[0].innerHTML.toString()
    var redx_val = new_arr.filter(ite => html_val.includes(ite))
    df.nextElementSibling.children[0].innerHTML = `(${dwidth}X${dheight})  ${redx_val[0]}`
}

try {
    callSize();
} catch (error) {
    console.log(error)
}

// YOU CAN MODIFY ABOVE CODE WITH YOUR WIS


    return (
        <></>
    )
}

export default FiveConcept;