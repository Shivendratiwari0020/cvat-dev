import React from 'react';
import { Checkbox, Row, Col } from 'antd';
// import '../../App.css'
import './AdditionalAttributes.css'
import { Button } from 'antd';
import serverProxy from '../../server-proxy';
import { useSelector } from 'react-redux'


type Props = {
  img_logo: string;
  img_name : string;
  attrid : any;
}

const AdditionalAttributes: React.FC<Props> = ({img_logo,img_name,attrid}:Props) => {
  const currentId = useSelector(state => state)
// const sendSignName = (sname:string,sid:number) => {
const sendSignName = (sname:string,sid:any) => {
  console.log(sname);
  debugger;
  // let new_array = [];
  // let new_array = 0;
  // let data = currentId.annotation.job.attributes;
  // for (let vv in data) {
  //   for (let nn in data[vv]){
  //     if(data[vv][nn].inputType == "catalogue"){
  //       new_array = data[vv][nn].id
  //       console.log(data[vv][nn].id)
  //       // new_array.push(data[vv][nn].id)
  //     }
  //   }
  // }
  // serverProxy.jobs.getUpdate(new_array,sname).then((res) => {
//     serverProxy.jobs.getUpdate(sid,sname).then((res) => {
//     console.log(res);
//     // setSigns(res)
//     location.reload()
// });

  attrid.changeAttribute(attrid.attrID,sname)

  // const url = `http://localhost:7000/api/cat/1/updata/?sname=${sname}`
  // fetch(url)
  // .then(resp => resp.json())
  // .then(res => console.log(res))
  //  window.location.reload();
}


  return (
    <div style={{ width: '50%' }} className="marginclass" style={{ padding: '10px' }}>
      <div id="additionalattributes" >
        <div ><b>ADDITIONAL ATTRIBUTES:</b></div>

        <div id="wrapper">



          <div id="div1" style={{ width: '50%' }}>
            <Checkbox.Group style={{ width: '100%' }} >
              <Row>
                <Col span={8}>
                  <Checkbox value="CONTAMINATED">CONTAMINATED</Checkbox>
                </Col>
              </Row>

              <Row>
                <Col span={8}>
                  <Checkbox value="DISABLED">DISABLED</Checkbox>
                </Col>
              </Row>

              <Row>
                <Col span={8}>
                  <Checkbox value="FLASHING">FLASHING</Checkbox>
                </Col>
              </Row>

              <Row>
                <Col span={8}>
                  <Checkbox value="FOR_OTHER_ROAD">FOR_OTHER_ROAD</Checkbox>
                </Col>
              </Row>
            </Checkbox.Group>

            <label htmlFor="invalid">INVALID</label>
            &nbsp;  <select name="invalid" id="invalid">
              <option value="none">none</option>

            </select>

            <br />

            <label htmlFor="invisible">INVISIBLE</label>
            &nbsp;  <select name="invisible" id="invisible">
              <option value="invisible_start">Invisible_start</option>

            </select>








            <Checkbox.Group style={{ width: '100%' }} >
              <Row>
                <Col span={8}>
                  <Checkbox value="PARTLY">PARTLY</Checkbox>
                </Col>
              </Row>
              <Row>
                <Col span={8}>
                  <Checkbox value="SIGN_EMBEDDED">SIGN_EMBEDDED</Checkbox>
                </Col>
              </Row>
            </Checkbox.Group>


            <label htmlFor="sign_lane_distance">SIGN_LANE_DISTANCE</label>
            &nbsp;  <select name="sign_lane_distance" id="sign_lane_distance">
              <option value="none">none</option>

            </select>


            <Checkbox.Group style={{ width: '100%' }} >
              <Row>
                <Col span={8}>
                  <Checkbox value="SIGN_ON_MULTI_SIGN_MOUNTING">SIGN_ON_MULTI_SIGN_MOUNTING</Checkbox>
                </Col>
              </Row>
              <Row>
                <Col span={8}>
                  <Checkbox value="TWISTED">TWISTED</Checkbox>
                </Col>
              </Row>
            </Checkbox.Group>
          </div>

          <div id="wrapper1">
            <div id="div2">
              <img
                width={150}
                alt="photograph sent from prev page"
                src=" "
                style={{ float: 'right' }}
              />
            </div>

            {/* <SignLogo/> */}

            <div id="div3">
            <div className='signimage'>
            <img src={img_logo} style={{width:"65px", height:"65px"}}/> <br />
            </div>
              <Button style={{"marginBottom":"2px", "backgroundColor":"green"}}>Full</Button>
              {/* <Button  style={{"marginBottom":"2px"}} onClick = {() => sendSignName(img_name,attrid.attrID)} >Ok</Button> */}
              <Button  style={{"marginBottom":"2px"}} onClick = {() => sendSignName(img_name,attrid)} >Ok</Button>
              <Button  style={{"marginBottom":"2px"}}>Apply</Button>


            </div>
          </div>

        </div>

      </div>
    </div>


  )
}

export default AdditionalAttributes