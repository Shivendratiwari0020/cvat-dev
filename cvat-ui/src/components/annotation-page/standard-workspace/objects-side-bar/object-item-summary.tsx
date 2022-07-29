import React, { useEffect, useState } from 'react';
import { Table, Tooltip } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Select } from 'antd';
import { Col, Row } from 'antd';
import { Input} from 'antd';
import { LeftCircleFilled, RightCircleFilled } from '@ant-design/icons';
import { Typography } from 'antd';
import serverProxy from 'cvat-core/src/server-proxy';
import { changeFrameAsync } from 'actions/annotation-actions';
import { useDispatch } from 'react-redux';

interface DataType {
        key: string;
        track: string;
        Category: string;
        frameCount: string;
        validationStatus: string;
        SignClass: string
    };

const { Title } = Typography;
const { Option } = Select;
const { Search } = Input;

const ObjectLabelSummary = () => {
    const [datas, setData] = useState([])  
      const [selectedRowData, setSelectedRowData] = useState<any>()
      const [search, setSearch] = useState(false)
      const [searchData, setSearchData] = useState([])
      const [searchValue, setSearchValue] = useState("")
      const [dropDownValue, setDropDownValue] = useState('trackId')
      const dispatch = useDispatch();


    const handleChange = (value: string) => {
        setDropDownValue(value)
      };

    const handleSearchChange = (event:any) => {
        if(event.target.value == ''){
            setSearch(false)
        }
        else{
        setSearchValue(event.target.value)
        }
    }
    
    const onSearch = (value: string) =>{
        if(searchValue == ''){
            setSearch(false)
        }
        else {
            setSearch(true)
            if(dropDownValue == 'trackId'){
                const filterSearchData = datas?.filter((item:any) => item.track_id == value);
                setSearchData(filterSearchData)
            }
            else if(dropDownValue == 'category'){
                const filterSearchData = datas?.filter((item:any) => item);
                setSearchData(filterSearchData)
            }
            else if(dropDownValue == 'signClass'){
                const filterSearchData = datas?.filter((item:any) => item.sign_class == value);
                setSearchData(filterSearchData)
            }
            
        }
    } 
   

    const handleLeftClick = (frame:any) => {
        dispatch(changeFrameAsync(frame));
    }
    const handleRightClick = (frame:any) => {
        dispatch(changeFrameAsync(frame));
    }

    const columns: ColumnsType<DataType> = [   
        {
          title: 'Track Id',
          dataIndex: 'track_id',
          render: (text:any) => <a>{text}</a>,
        },
        {
          title: 'Object Category',
          className: 'column-money',
          dataIndex: 'label',
          align: 'right',
        },
        {
          title: 'Frame Count',
          dataIndex: 'count',
        },
        {
          title: 'Navigation',
          dataIndex: 'start_frame',
          render: () => <a>
                        <Tooltip title={selectedRowData?.start_frame} ><LeftCircleFilled style={{marginRight: '10px'}} onClick={() => handleLeftClick(selectedRowData?.start_frame)} /></Tooltip> 
                        <Tooltip title={selectedRowData?.end_frame} ><RightCircleFilled onClick={() => handleRightClick(selectedRowData?.end_frame)} /></Tooltip>
                    </a>,
        },
        {
          title: 'Sign Class',
          dataIndex: 'sign_class',
        },
      ];

    useEffect(() => {
        let path = window.location.pathname;
        let pathArr = path.split("/");
        serverProxy.jobs.getTrackedFrameSummary(Number(pathArr[pathArr.length - 1])).then((res:any) => {
            setData(res);
        });

    },[])
   

    return (
        <>
            <Row>
                <Col span={24}>
                <Title level={5}>Total Frame Count : 112</Title>
                </Col>
            </Row>
            <Row>
                <Col span={10}>
                    <Select defaultValue="trackId" style={{ width: 120 }} onChange={handleChange}>
                        <Option value="trackId">Track Id</Option>
                        <Option value="category">Object Category</Option>           
                        <Option value="signClass">Sign Class</Option>
                    </Select>
                </Col>
                <Col span={4} />
                <Col span={10}>
                <Search placeholder="search" onChange={handleSearchChange} onSearch={onSearch} enterButton />
                </Col>                
            </Row>
           
            <Table
                columns={columns}
                dataSource={search ? searchData : datas}
                bordered
                pagination={false}
                scroll={{x:true}}
                onRow={(record:any) => {
                    return { 
                        onMouseEnter: () => {
                            setSelectedRowData(record)
                        }, 
                    };
                  }}
            />
    </>

    )
}

export default ObjectLabelSummary;