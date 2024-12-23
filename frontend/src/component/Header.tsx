import React from "react";
import { Menu} from "antd";
import SubMenu from "antd/es/menu/SubMenu";
import {Link} from "react-router-dom";

const Header: React.FC = () => {
    return (
        <div className="header">
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1-1"]}>
            {/*<SubMenu key="1" title="Written Exam">*/}
            {/*    <Menu.Item key="1-1">*/}
            {/*        <Link to="/index/QusetionStart">Qusetions Start</Link>*/}
            {/*    </Menu.Item>*/}
            {/*    <Menu.Item key="1-2">*/}
            {/*        <Link to="/index/Record">Record</Link>*/}
            {/*    </Menu.Item>*/}
            {/*</SubMenu>*/}
            <Menu.Item key="1-1">
                <Link to="/index/ExamPage">Exam</Link>
            </Menu.Item>
            <Menu.Item key="2-1">
                <Link to="/index/InterviewPage">Interview</Link>
            </Menu.Item>
            <Menu.Item key="3-1">
                <Link to="/index/SchedulePage">Schedule</Link>
            </Menu.Item>
        </Menu>

        </div>
    );
};

export default Header;
