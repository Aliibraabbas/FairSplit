import { Outlet } from 'react-router-dom'

function MainLayout() {
  return (
    <div className="main-layout">
      <header>
        <nav>
          {/* Navigation will be added later */}
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer>
        {/* Footer content */}
      </footer>
    </div>
  )
}

export default MainLayout
