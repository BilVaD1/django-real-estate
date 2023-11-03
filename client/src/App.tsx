import { Layout } from "antd"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import AppFooter from "./components/common/AppFooter"
import AppHeader from "./components/common/AppHeader"
import Homepage from "./pages/Homepage"
import ProperyListPage from "./pages/ProperyListPage"

const {Content, Header, Footer} = Layout


function App() {

  return (
    <Router>
      <Layout className="main-layout">
        <Header>
          <AppHeader />
        </Header>
        <Content>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path='/properties' element={<ProperyListPage />}/>
          </Routes>
        </Content>
        <Footer>
          <AppFooter />
        </Footer>
      </Layout>
    </ Router>
  )
}

export default App
