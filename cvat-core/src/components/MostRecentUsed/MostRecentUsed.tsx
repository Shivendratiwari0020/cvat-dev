
import React from 'react'
import './MostRecentUsed.css'
// import '../../App.css'

const MostRecentUsed : React.FC = () => {

  const myStyle={
    width: '100%',
    border: '1px solid grey',
    minHeight:'10vh'
  }

  return (
      <>
    <div className="marginclass">
      <div>Most Recent Used</div>

      <div className="mostrecentData" style={myStyle}>


      </div>



</div>


     </>
  )
}

export default MostRecentUsed