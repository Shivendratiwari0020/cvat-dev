import React, { useEffect, useState } from 'react'
import './SignGroups.css'
// import server-proxy from './cvat/cvat-core/src/server-proxy.js'
// import serverProxy from "/home/srv005/cvat/cvat-core/src/server-proxy.js"
//const serverProxy=require(""./server-proxy")
import serverProxy from "../../../../cvat-core/src/server-proxy"
import { Checkbox, Row, Col } from 'antd';
// import serverProxy from "../../../../../../../../cvat-core/src/server-proxy"
// import serverProxy from '../../server-proxy'


const SignGroups: React.FC = () => {
  const [signs, setSigns] = useState([]);

  const myStyle = {
    width: '100%',
    border: '1px solid grey',
    margin: 'auto',
    marginTop: '10px',
    minHeight: '95vh'

  }


  const RenderNode = (data) => {
    return data.data.map((item, index) => {
      return <h1 key={index}>{item.folder_name}</h1>;
    });
  };

  useEffect(() => {
    // const signs = [
    //   {
    //   "projectid": 59,
    //   "folder_name": "Blue Round Signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Diamond Signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Diverse round signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "No Overtaking"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "No Signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "ROOT"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Rectangular signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Red Round Signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Speed Limit Ends Inversed"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Speed Limit Ends"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Speed Limits Inversed"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Speed Limits"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Supplementary Signs NOT containing pictures"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Supplementary signs containing CHN,JPN,KOR scripts"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Supplementary signs containing TexRegExp"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Supplementary signs containing pictures"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "Triangular signs"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "US Speed Limit Diamond"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "US Speed Limit End"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "US Speed Limit Inversed"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "US Speed Limit with colorful Background"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "US Speed Limits with White Background"
    //   },
    //   {
    //   "projectid": 59,
    //   "folder_name": "US other signs"
    //   }]

    // const signs = serverProxy.jobs.getcatalog(1)

    serverProxy.jobs.getcatalog(60).then((res) => {
      console.log(res);
      setSigns(res)
    });
  },[]);




  return (
    <>
      <div style={{ minHeight: '95vh' }} className="marginclass">
        <div >Sign Groups </div>
        <div id="SignGroups" style={myStyle}>
        <RenderNode data={signs} />

        </div>

      </div>
    </>
  )
}

export default SignGroups


