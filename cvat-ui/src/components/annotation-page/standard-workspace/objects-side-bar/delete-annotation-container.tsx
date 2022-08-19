// Copyright (C) 2020-2021 Intel Corporation
//
// SPDX-License-Identifier: MIT

import React, { useState } from 'react';
import { Row, Col } from 'antd/lib/grid';
import { Radio } from "antd";


interface Props {
    option: number;
    hide(): void;
    show(): void;
    handleOptionSelect(): void;
    setOption(): void;
}





function DeleteAnnotationContainer(props: Props): JSX.Element {
    // const { readonly, objectType, shapeType } = props;
    // const [option, setOption] = useState<Props>(3);
    const handleOption = (e: Object): any => {  
        console.log("option selected at event",e.target.value);
        // props.setOption(e.target.value);
        props.handleOptionSelect(e.target.value)
        // return `${ username } scored ${ points } points!`;  
      } 

    return (
        <Row align='middle' justify='space-between'>
            <div className="delete-head">
                <p>Single ROI for deletion</p>
            </div>
            <Radio.Group
            className="radio-container"
            onChange={handleOption}
            value={props.option}
            >
                <Radio value={"current-frame"}>Current Frame</Radio>
                <Radio value={"current-frame-to-end-frame"}>Current Frame to End Frame</Radio>
                <Radio value={"start-frame-to-current-frame"}>Start Frame to Current Frame</Radio>
                <Radio value={"start-frame-to-end-frame"}>Start Frame to End Frame</Radio>
                <Radio value={"custom-range"}>
                    Enter Start Frame &nbsp;
                    <input type="number" className="frame-range" value="31" /> to End
                    &nbsp;Frame &nbsp;
                    <input type="number" className="frame-range" value="1200" />
                </Radio>
            </Radio.Group>
        </Row>
    );
}

export default React.memo(DeleteAnnotationContainer);
