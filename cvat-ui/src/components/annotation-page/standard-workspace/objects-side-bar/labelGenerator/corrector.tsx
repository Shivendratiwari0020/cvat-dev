import React, { useEffect, useState } from 'react'
import { Modal, Col, Row, Divider, Input, Popover, Button } from 'antd';
import { DotChartOutlined } from "@ant-design/icons";
import {  Typography, Radio } from 'antd';
import {  useDispatch } from 'react-redux';
import { saveAnnotationsAsync } from 'actions/annotation-actions';
import { useSelector } from "react-redux";
import serverProxy from "cvat-core/src/server-proxy";
import './context_menu.css';
import NotSavedAnnotationModal from '../object-item-not-saved-annotations';


const style: React.CSSProperties = { padding: '8px 0', height: '200px', width: '200px' };
const menu_div_style: React.CSSProperties = { display: 'inline-grid' };

interface Props {
    AnnotationId: number |  undefined
    attributes: any[];
    jobInstance:any;
    popOverHide: (a: boolean) => void;

}


const { Title } = Typography;


const Corrector = (props:Props) => {
    //const [visible, setVisible] = useState(false);
    
    const {attributes, AnnotationId, jobInstance} = props
    console.log('Corrector    props', jobInstance)
    const dispatch = useDispatch();
    const [cssclass, setCssclass] = useState("");
    const [assignSRdata, setAssignSRdata] = useState([]);
    const currentJob = useSelector((state) => state);
    const [croppedimages, setCropedImages] = useState([])
    const [rightClick, setRightClick] = useState(false)
    const [visible, setVisible] = useState(false);
    const [frameId, setFrameId] = useState<any>([])
    const [flag, setFlag] = useState(false)
    const [id, setId] = useState()
    const [jobId, setJobId] = useState(0);
    const [flagValue, setFlagValue] = useState(false)
   
    React.useEffect(() => {
      let path = window.location.pathname;
      let pathArr = path.split("/");
      setJobId(Number(pathArr[pathArr.length - 1]));
    }, []);

    const hide = () => {
      setVisible(false);
    };
  
    const handleVisibleChange = (newVisible: boolean) => {
      setVisible(newVisible);
    };

    const callSave = () => {
        if(AnnotationId == undefined){
            setFlagValue(true)
        }
        else{
        setVisible(true);
        // need to see
        // 64 is job id, 12 is task_id is annotation id 
        serverProxy.jobs.labelCorrectorImages(jobId, AnnotationId).then((res) => {
            setCropedImages(res);
        });
        getAssignSRdata();
    }

    };

    // document.addEventListener('keydown', (event) => {
    //     if (event.key == 'w') {
    //         callSave();
    //     }
    // })
    
    const handleRightClick = (event: { preventDefault: () => void; type: string; }, id) => {
        event.preventDefault();         
        if(event.type == 'contextmenu'){
           //setFrameId([...frameId, id])
           setId(id)
           console.log("contextmenu")
            setRightClick(true);
            //setFlag(false)
        }
        else {
            setRightClick(false)
        }    
    }

    const handleRightClickPop = () =>{
        setRightClick(false)
    }

    const updateCss = (e:any,frame:any) => {
        alert("bingo")
        console.log(frame)
        if (cssclass == "") {
            setCssclass('container_menu')
        } else {
            setCssclass('')
        }
    }

    const getAssignSRdata = () => {
        const { annotation: {
            job: {
                requestedId, ...ononrest
            }, ...onrest
        }, ...rest } = currentJob;

        serverProxy.jobs.getCorrectorData(requestedId).then((res) => {
            console.log(res)
            console.log("res")
            setAssignSRdata(res);
        });
    }

    // useEffect(() => {
    //     getAssignSRdata();
    // }, [])
    const srLabelPostApi = async (payload) => {
        return serverProxy.jobs
        .saveLabelCorrectorAttributeData(payload)
          .then((result: any) => {
            return result;
          })
          .catch((error: any) => {
            return error;
          })
      }

      const srInvisiblePostAPI = async (payload) => {
        return serverProxy.jobs
        .saveSrInvisibleLabelCorrectorAttributeData(payload)
          .then((result: any) => {
            return result;
          })
          .catch((error: any) => {
            return error;
          })
      }
      //saveSrInvisibleLabelCorrectorAttributeData
    
    const handleButtonClick = async(value:any, id:any) => {
        const attributesFilterData = attributes.filter((item:any) => assignSRdata.includes(item.name))
        const finalFilterData = attributesFilterData.filter(item => item.name == value)
        // const cc = aaa.includes(value);
         console.log("finalFilterData", finalFilterData)
        if(value == 'SR_PARTLY'){       
            setFlag(true)   
            setFrameId([...frameId, id])  
            setRightClick(false) 
            try {   
                const payload = {
                    track_id: AnnotationId,
                    AnnotationId: AnnotationId,
                    frame:id,
                    attribute_name: finalFilterData[0].name,
                    attribute_val :'true',
                    attribute_id : finalFilterData[0].id,
                    attributre_previous_value: finalFilterData[0].values[0].toLocaleLowerCase()
                }           
          
                const apiResponse = await srLabelPostApi(payload);
                console.log('apiResponse', apiResponse)
              } catch (err) {
                console.log(err);
              }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        }
        else if(value == 'SR_INVISIBLE'){
            setRightClick(false) 
            try {   
                const payload = {
                    track_id: AnnotationId,
                    AnnotationId: AnnotationId,
                    frame:id,
                    attribute_name: finalFilterData[0].name,
                    attribute_val :'Invisible_Start',
                    attribute_id : finalFilterData[0].id,
                    attributre_previous_value: finalFilterData[0].values
                }           
          
                const apiResponse = await srInvisiblePostAPI(payload);
                console.log('apiResponse', apiResponse)
              } catch (err) {
                console.log(err);
            }  
        }
    }
    const AssignNode = ({data,frame}) => {
        return data.map((item: any) => {
            return (
                // <MenuItem key={item} onClick={(e)=>{updateCss(e,frame) ,alert("clicked me")} }>
                    // <FaEllipsisV className="openwith"/>
                    // <span id = {frame}>{item}</span>
                    <div>
                        <Button onClick={() =>handleButtonClick(item, frame)} style={{marginBottom:'10px'}} type='text' id={frame}>{item}</Button>
                    </div>
                    // {/* <span onClick={updateCss}>Partly visible</span> */}
                // </MenuItem>
            )
        })
    }

    const CropedImagesNode = (data: any) => {
        return data.data.map(item => {
            return (
                <Col span={6} key={item.frame}>
                   
                    <Popover
                        content={<AssignNode data={assignSRdata} frame={item.frame}/>}
                        placement="rightTop"
                        title=""                       
                        trigger="click"
                        visible={rightClick && id == item.frame}
                        >
                            <div 
                                className={flag && frameId.includes(item.frame) ? 'container_menu' : ''  }
                                onClick={handleRightClickPop}
                                onContextMenu={(event) =>handleRightClick(event, item.frame)}
                            >
                                <img   style={style} src={item.img_base64}/>
                                
                            </div>
                            <span>Frame No. {item.frame}</span>                            
                    </Popover>
                    {/* </ContextMenuTrigger> */}
                    {/* // <ContextMenu id={"contextmenu_"+item.frame}> */}
                        
                    {/* </ContextMenu> */}
                </Col>
            )
        })

    }
  
   

    const bulkUpdateAttributes = async () => {
        await  dispatch(saveAnnotationsAsync(jobInstance));
       window.location.reload();
       setFlagValue(false);
    };

    const handleCancel = () => {
        setFlagValue(false);
    };

    const popOverHide = (a: boolean) =>{
        setFlagValue(a)
    }
    const handleOk = () => {
        setVisible(false)
        window.location.reload();
    }

    return (
        <>
            <DotChartOutlined onClick={callSave} />
            {flagValue  ?             
                <>
                <NotSavedAnnotationModal flagValue={true} popOverHide={popOverHide} jobInstance={jobInstance} />

                </>
            :
            <Modal
                title="Label Corrector"
                centered
                visible={visible}
                onOk={handleOk}
                onCancel={() => setVisible(false)}
                width={1000}
            >
                <Row gutter={[16, 24]}>

                    <Col className="gutter-row" span={6}>
                        <div style={menu_div_style}>
                            Frame No <Input size="small" />
                        </div>
                    </Col>
                    <Col className="gutter-row" span={6}>
                        <div style={menu_div_style}>
                            Step Filter <Input size="small" />
                        </div>
                    </Col>
                </Row>
                <Divider orientation="left">Corrector</Divider>
                <Row>
                    <CropedImagesNode data={croppedimages} />
                </Row>
            </Modal>
            }
        </>
    )
}

export default Corrector;