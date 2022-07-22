import React, { useState } from 'react';
import axios from 'axios';
import { Button, Divider, Modal, Typography, Radio } from 'antd';
import {  useDispatch } from 'react-redux';
import { saveAnnotationsAsync } from 'actions/annotation-actions';
import { CombinedState } from 'reducers/interfaces';


interface Props {
    popOverHide: (a: boolean) => void;
    jobInstance: any;
    flagValue: boolean
}


const NotSavedAnnotationModal = (props: Props) => {
    const dispatch = useDispatch();
    const { Title } = Typography;
    const [isModalVisible, setIsModalVisible] = useState(false);

    const showModal = async () => {
        setIsModalVisible(true);
        props.popOverHide(false);
    };

    const bulkUpdateAttributes = async () => {
        await  dispatch(saveAnnotationsAsync(props.jobInstance));
       window.location.reload();
        setIsModalVisible(false);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    return (
        <>
            {props.flagValue ?
                <>
                <Modal width={650} title="Please save the annoation" visible={true} onOk={bulkUpdateAttributes} onCancel={handleCancel}>
                    <Title level={5} style={{ display: 'block', textAlign: 'center'}}> Do you want to save the Annotation?</Title>
                </Modal>
            </>
            :
            <>
            <Button type="text" onClick={showModal}>Bulk Update</Button>
           
                <>
                    <Modal width={650} title="Please save the annoation" visible={isModalVisible} onOk={bulkUpdateAttributes} onCancel={handleCancel}>
                        <Title level={5} style={{ display: 'block', textAlign: 'center'}}> Do you want to save the Annotation?</Title>
                    </Modal>
                </>
            
            </>
        }
        </>

    )
};

export default NotSavedAnnotationModal;