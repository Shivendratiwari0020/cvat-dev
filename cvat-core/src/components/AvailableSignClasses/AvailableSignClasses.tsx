import React,{useEffect} from 'react'
//import server-proxy from './cvat/cvat-core/src/server-proxy.js'
// import serverProxy from '../../../server-proxy'./../
//import serverProxy from "/home/srv005/cvat/cvat-core/src/server-proxy.js"
// import serverProxy from '../../server-proxy';
 //import serverProxy from "../../../../../../../../cvat-core/src/server-proxy"

const AvailableSignClasses  : React.FC = () => {

  const myStyle={
    width: '100%',
    border: '1px solid grey',
    minHeight:'45vh'
  }

/*
  useEffect(  ()=>
  {
    //const result =  serverProxy.getData();

    // const result= fetch(`localhost:7000/cat/59/`);
    // console.log(result);
  fetch('http://localhost:8080/api/v1/projects')
  .then(response => response.json())
  .then(json => console.log(json))

  }
  ,[] ) ; */

  useEffect(  ()=>
  {
    // const result =  serverProxy.server.populateData();
    console.log("result");
  }
  ,[] ) ;



  return (
      <>
    <div className="marginclass" >
      <div> Available Sign Classes</div>


    <div id="Sign classes" style={myStyle}>


    </div>

    </div>
    </>
      )
}

export default AvailableSignClasses