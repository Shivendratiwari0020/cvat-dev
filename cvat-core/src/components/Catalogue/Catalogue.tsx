import React, { useState } from 'react';
import 'antd/dist/antd.css';
import { Modal, Button } from 'antd';
import { Layout } from 'antd';
import SignGroups from '../SignGroups/SignGroups';
import SearchSign from '../SearchSign/SearchSign';
import MostRecentUsed from '../MostRecentUsed/MostRecentUsed';
import AvailableSignClasses from '../AvailableSignClasses/AvailableSignClasses';
import DescriptionWindow from '../DescriptionWindow/DescriptionWindow';
import AdditionalAttributes from '../AdditionalAttributes/AdditionalAttributes';

import './Catalogue.css'
import { Interface } from 'readline';


const { Sider, Content } = Layout;


const Catalogue: React.FC<{}> = (props) => {

    const [isModalVisible, setIsModalVisible] = useState(false);

    const showModal = () => {
      setIsModalVisible(true);
    };

    const handleOk = () => {
      setIsModalVisible(false);
    };
    return (
        <div className="marginclass">
             <Button type="primary" onClick={showModal}>
        Catalogue
      </Button>
      <Modal visible={isModalVisible} onOk={handleOk} width={1300} bodyStyle={{height: 750}}>
      <Layout>
      <Sider width={300} style={{ minHeight: '100vh' , backgroundColor: 'white'}}>
      <SearchSign/> <SignGroups p/>
     </Sider>
      <Layout>
        <div style={{ minHeight: '17vh', width:'100%' }}><MostRecentUsed/></div>
        <Content width={500} > <AvailableSignClasses/></Content>
              <div id="footerLayout" style={{width:'100%'}} >
            <DescriptionWindow/>
            <AdditionalAttributes />
            </div>
      </Layout>
    </Layout>
      </Modal>
        </div>
    );
};

export default Catalogue;