import React,{useEffect} from 'react';
import { Input } from 'antd';
import './SearchSign.css'
// import '../../App.css';

const SearchSign : React.FC  = () => {
  return (
    <div className="marginclass" style={{ minHeight: '10vh'} }>

    <Input placeholder="Search Sign" />

    </div>
  )
}

export default SearchSign
