import React,{useEffect } from "react";
import { useSelector } from "react-redux";

import "./index.css";

type Props = {
    clientID : number,
}

const Canvass: React.FC<Props>  = ({ clientID }: Props) => {
    const currentJob = useSelector((state) => state);

    useEffect(() => {
        const points =  currentJob.annotation.canvas.instance.view.drawnStates[clientID].points
        console.log(points)
        let sourceCanvas=document.getElementById("cvat_canvas_background");
        if(sourceCanvas){
            const sourceContext=sourceCanvas.getContext("2d");
            const destinationCanvas=document.getElementById(`display_part_sign_image${clientID}`);
            const destinationContext=destinationCanvas.getContext("2d");
            // destinationContext.drawImage(sourceCanvas,600,500, 300, 300, 0, 0, 300, 300);
            console.log(points[0], points[1], points[2]-points[0], points[3]-points[1], 0, 0, 300, 300)
            destinationContext.drawImage(sourceCanvas,points[0], points[1], points[2]-points[0], points[3]-points[1], 0, 0, 150, 150);
          }

    },[]);

    return <canvas id={`display_part_sign_image${clientID}`} className="display_part_sign_image_class"></canvas>
}

export default Canvass;

