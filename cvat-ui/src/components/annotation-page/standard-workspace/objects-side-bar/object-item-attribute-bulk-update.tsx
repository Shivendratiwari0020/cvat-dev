import React, { useState } from 'react';
import { Button, Divider, Modal, Typography, Radio } from 'antd';
import {useDispatch } from 'react-redux';
import InputNumber from 'antd/lib/input-number';
import { Checkbox } from 'antd';
import type { CheckboxChangeEvent } from 'antd/es/checkbox';
import type { RadioChangeEvent } from 'antd';
import serverProxy from 'cvat-core/src/server-proxy.js';
import { saveAnnotationsAsync } from 'actions/annotation-actions';

interface Props {
  attrID: number;
  attrName: string;
  trackId: number;
  popOverHide: (a: boolean) => void;
  jobInstance: any;
  AnnotationId: number | undefined
  attrValue: any;
}
interface payLoadProps {
  start_frame: any;
  end_frame: any;
  job_id: any;
  AnnotationId: number| undefined;
  attribute_id: number,
  attribute_name: string;
  attribute_val: any;
  attribute_previous_val:any
}

const AttributeBulkUpdate = (props: Props) => {
    const dispatch = useDispatch();
  const {attrID, AnnotationId, attrValue, attrName, trackId, jobInstance } = props;
  const { Title } = Typography;
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [value, setValue] = useState(1);
  const [chkValue, setChkValue] = useState(false);
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [jobId, setJobId] = useState(0);
  const [err,setErr] = useState(false);

  React.useEffect(() => {
    let path = window.location.pathname;
    let pathArr = path.split("/");
    setJobId(Number(pathArr[pathArr.length - 1]));
  }, []);

  const onRadioChange = (e: RadioChangeEvent) => {
    setValue(e.target.value);
    if(e.target.value === 4){
      setStart(null);
      setEnd(null);
    }
  };

  React.useEffect(() => {
    //Don't know how to find the currentFrame number , so default it to 1
    let currentFrame = 1;
    if (value == 1) {
      setStart(currentFrame);
      setEnd(10);
    } else if (value == 2) {
      setStart(1);
      setEnd(currentFrame);
    } else if (value == 3) {
      setStart(1);
      setEnd(10);
    }
  }, [value]);

  const onChange = (e: CheckboxChangeEvent) => {
    setChkValue(e.target.checked);
  };

  const showModal = async () => {
   
    setIsModalVisible(true);
    props.popOverHide(false);
  };
  

  const payLoadPostAPI = async (payload: payLoadProps) => {
    return serverProxy.jobs
    .saveBulkupdate(payload)
      .then((result: any) => {
        return result;
      })
      .catch((error: any) => {
        return error;
      })
  }

  const bulkUpdateAttributes = async () => {
    
      // here we need to call save function
    if(start !== null && end !== null){
        await dispatch(saveAnnotationsAsync(jobInstance))
      try {
        const payLoad: payLoadProps = {
          start_frame: start,
          end_frame: end,
          job_id: jobId,
          AnnotationId,
          attribute_id: attrID,
          attribute_name: attrName,
          attribute_previous_val: attrValue.toString().toLocaleLowerCase(),
          attribute_val: chkValue.toString().toLocaleLowerCase()
        };
  
        const apiResponse = await payLoadPostAPI(payLoad);
        if(apiResponse.message ==  "true"){
          window.location.reload();
        }

        setIsModalVisible(false);
      } catch (err) {
        console.log(err);
      }
    }else{
      setErr(true);
      setTimeout(()=>{
        setErr(false);
      },3000);
    }
  };

  const handleCancel = () => {
    setIsModalVisible(false);
  };

  return (
    <>
      <Button type="text" onClick={showModal}>Bulk Update</Button>
      {isModalVisible &&
        <>
          <Modal width={650} title="Bulk Update Object Labels" visible={isModalVisible} onOk={bulkUpdateAttributes} onCancel={handleCancel}>
            <Title level={5} style={{ display: 'block', textAlign: 'center' }}> Track Id: {trackId}</Title>
            <Divider />
            <Radio.Group onChange={onRadioChange} value={value} style={{ borderLeft: '1px solid grey', borderTop: '1px solid grey', padding: '10px' }}>
              <React.Fragment>
                <Radio value={1}><Title level={5}>Current Frame to End Frame</Title></Radio>
              </React.Fragment>
              <div>
                <Radio value={2}> <Title level={5}>Start Frame to Current Frame</Title></Radio>
              </div>
              <React.Fragment>
                <Radio value={3}><Title level={5}>Start Frame to End Frame</Title></Radio>
              </React.Fragment>
              <div style={{ display: 'flex', alignItems: 'baseline' }}>
                <Radio value={4} />
                <Title level={5}>Enter Start Frame</Title>
                <InputNumber disabled={value !==4} style={{ marginLeft: '10px' }}  min={1} onChange={(value:number) => setStart(value)} />
                <Title style={{ marginLeft: '10px' }} level={5}>to End Frame</Title>
                <InputNumber disabled={value !==4} style={{ marginLeft: '10px' }}  min={start} onChange={(value: number) => setEnd(value)} />
              </div>
            </Radio.Group>
            {err ? <Title level={5} style={{color:'red'}}>Please select start & end frame,before proceeding!</Title> : ''}
            <Divider />
            <div style={{ display: 'flex', marginTop: '20px', alignItems: 'flex-start' }}>
              <table style={{ border: '1px solid grey' }}>
                <tr style={{ border: '1px solid grey' }}>
                  <th style={{ border: '1px solid grey', padding: '10px' }}><Title level={5}>Attributes</Title></th>
                  <th style={{ border: '1px solid grey', padding: '10px' }}><Title level={5}>Value</Title></th>
                </tr>
                <tr style={{ border: '1px solid grey' }}>
                  <td style={{ border: '1px solid grey', padding: '10px' }}><Title style={{ marginRight: '20px' }} level={5} >{attrName}</Title></td>
                  <td style={{ border: '1px solid grey', padding: '10px' }}> <Checkbox onChange={onChange} /></td>
                </tr>
              </table>              
            </div>

          </Modal>
        </>
      }
    </>
  )
};
export default AttributeBulkUpdate;