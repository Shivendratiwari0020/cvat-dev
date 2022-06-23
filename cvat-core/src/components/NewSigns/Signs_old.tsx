import React, { useState, useEffect } from "react";
import { Modal, Button } from "antd";
import "antd/dist/antd.css";
import "./index.css";
import { Layout, Input, Card } from "antd";
import { RadiusUprightOutlined } from "@ant-design/icons";
import serverProxy from "../../../../cvat-core/src/server-proxy";
import { useSelector } from "react-redux";
import ReactHtmlParser from "react-html-parser";
import { Checkbox, Row, Col } from "antd";

const { Sider, Content } = Layout;
const { Search } = Input;

type Props = {
  attrid: any,
};

const Signs: React.FC<Props> = ({ attrid }: Props) => {
  const [visible, setVisible] = useState(false);
  const [signs, setSigns] = useState([]);
  const [searchsigns, setSearchsigns] = useState([]);
  const [asigns, setaSigns] = useState([]);
  const [description, setDescription] = useState("");
  const [imgattr, setImgattr] = useState("");
  const [imgname, setImgname] = useState("");
  const currentJob = useSelector((state) => state);

  useEffect(() => {
    serverProxy.jobs
      .getcatalog(currentJob.annotation.job.requestedId)
      .then((res) => {
        setSigns(res);
      });
  }, []);

  const RenderNode = (data) => {
    return data.data.map((item, index) => {
      return (
        <div key={index}>
          <Button
            type="text"
            key={index}
            onClick={() => SignsNode(item.projectid, item.folder_name)}
            style={{ marginBottom: "3px" }}
          >
            {item.folder_name}
          </Button>{" "}
          <br />
        </div>
      );
    });
  };

  const SignsNode = (pid, fname) => {
    serverProxy.jobs.getPopulate(pid, fname).then((res) => {
      setaSigns(res);
    });
  };

  const SignRenderNode = (data) => {
    return data.data.map((obj) =>
      Object.entries(obj).map(([key, value]) => (
        <div key={key}>
          <img
            src={value.imagepath}
            onClick={() => {
              setDescription(value.description),
                setImgattr(value.imagepath),
                setImgname(value.signname);
            }}
            className="signs"
          />
        </div>
      ))
    );
  };

  const sendSignName = (sname: string, sid: any) => {
    attrid.changeAttribute(attrid.attrID, sname);
    setVisible(false);
  };

  const SearchNode = (e) => {
    const value = e.target.value.toLowerCase();
    let newarr = [];
    if (value.length > 2) {
      newarr = signs.filter((item) => {
        if (item.folder_name.toLowerCase().includes(value)) {
          return item;
        }
      });
      setSearchsigns(newarr);
    }
    return newarr;
  };

  const callSave = () => {
    setVisible(true);
  };

  return (
    <>
      <RadiusUprightOutlined onClick={callSave} />
      <Modal
        title=""
        centered
        visible={visible}
        onOk={() => setVisible(false)}
        onCancel={() => setVisible(false)}
        width={1350}
      >
        <>
          <Layout>
            <Sider width="350">
              <Card>
                <Search
                  placeholder="input search loading default"
                  style={{ marginBottom: "20px" }}
                  onKeyUp={(e) => SearchNode(e)}
                ></Search>
                <br />
                {searchsigns.length ? (
                  <div className="render" style={{ width: "100%" }}>
                    <RenderNode data={searchsigns} />
                  </div>
                ) : (
                  <div className="render">
                    <RenderNode data={signs} />
                  </div>
                )}
              </Card>
            </Sider>
            <Layout>
              <Content>
                <hr />
                <div className="ex3">
                  <SignRenderNode data={asigns} />
                </div>
                <div className="flexdivs">
                  <div className="description">
                    {ReactHtmlParser(description.split("\n").join(""))}
                  </div>
                  <div className="additionattr">
                    <div
                      style={{ width: "50%" }}
                      className="marginclass"
                      style={{ padding: "10px" }}
                    >
                      <div id="additionalattributes">
                        <div>
                          <b>ADDITIONAL ATTRIBUTES:</b>
                        </div>

                        <div id="wrapper">
                          <div id="div1" style={{ width: "50%" }}>
                            <Checkbox.Group style={{ width: "100%" }}>
                              <Row>
                                <Col span={8}>
                                  <Checkbox value="CONTAMINATED">
                                    CONTAMINATED
                                  </Checkbox>
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
                                  <Checkbox value="FOR_OTHER_ROAD">
                                    FOR_OTHER_ROAD
                                  </Checkbox>
                                </Col>
                              </Row>
                            </Checkbox.Group>
                            <label htmlFor="invalid">INVALID</label>
                            &nbsp;{" "}
                            <select name="invalid" id="invalid">
                              <option value="none">none</option>
                            </select>
                            <br />
                            <label htmlFor="invisible">INVISIBLE</label>
                            &nbsp;{" "}
                            <select name="invisible" id="invisible">
                              <option value="invisible_start">
                                Invisible_start
                              </option>
                            </select>
                            <Checkbox.Group style={{ width: "100%" }}>
                              <Row>
                                <Col span={8}>
                                  <Checkbox value="PARTLY">PARTLY</Checkbox>
                                </Col>
                              </Row>
                              <Row>
                                <Col span={8}>
                                  <Checkbox value="SIGN_EMBEDDED">
                                    SIGN_EMBEDDED
                                  </Checkbox>
                                </Col>
                              </Row>
                            </Checkbox.Group>
                            <label htmlFor="sign_lane_distance">
                              SIGN_LANE_DISTANCE
                            </label>
                            &nbsp;{" "}
                            <select
                              name="sign_lane_distance"
                              id="sign_lane_distance"
                            >
                              <option value="none">none</option>
                            </select>
                            <Checkbox.Group style={{ width: "100%" }}>
                              <Row>
                                <Col span={8}>
                                  <Checkbox value="SIGN_ON_MULTI_SIGN_MOUNTING">
                                    SIGN_ON_MULTI_SIGN_MOUNTING
                                  </Checkbox>
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
                                style={{ float: "right" }}
                              />
                            </div>
                            <div id="div3">
                              <div className="signimage">
                                <img
                                  src={imgattr}
                                  style={{ width: "65px", height: "65px" }}
                                />{" "}
                                <br />
                              </div>
                              <Button
                                style={{
                                  marginBottom: "2px",
                                  backgroundColor: "green",
                                }}
                              >
                                Full
                              </Button>
                              <Button
                                style={{ marginBottom: "2px" }}
                                onClick={() => sendSignName(imgname, attrid)}
                              >
                                Ok
                              </Button>
                              <Button style={{ marginBottom: "2px" }}>
                                Apply
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Content>
            </Layout>
          </Layout>
        </>
      </Modal>
    </>
  );
};

export default Signs;
