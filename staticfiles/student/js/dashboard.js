
// Move theme loading to run immediately, before DOM content loads
;(() => {
  const savedTheme = localStorage.getItem("dashboard-theme")
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
  const theme = savedTheme || (prefersDark ? "dark" : "light")

  document.documentElement.setAttribute("data-theme", theme)

  // Save the initial theme if not already saved
  if (!savedTheme) {
    localStorage.setItem("dashboard-theme", theme)
  }
})()

class TeacherDashboard {
  constructor() {
    this.init()
  }

  init() {
    this.setupThemeToggle()
    this.setupMobileMenu()
    this.setupNavigation()
    // this.setupNotifications() — removed to fix crash
    this.ensureThemeLoaded()
    this.addInteractiveEffects()
  }

  ensureThemeLoaded() {
    const currentTheme = document.documentElement.getAttribute("data-theme")
    const savedTheme = localStorage.getItem("dashboard-theme")

    if (!currentTheme && savedTheme) {
      document.documentElement.setAttribute("data-theme", savedTheme)
    }
  }

  toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme") || "light"
    const newTheme = currentTheme === "dark" ? "light" : "dark"

    document.documentElement.setAttribute("data-theme", newTheme)
    localStorage.setItem("dashboard-theme", newTheme)

    document.body.style.transition = "background-color 0.3s ease"
    setTimeout(() => {
      document.body.style.transition = ""
    }, 300)

    this.showToast(`Switched to ${newTheme} theme`)
  }

  setupMobileMenu() {
    const menuToggle = document.getElementById("menuToggle")
    const sidebar = document.getElementById("sidebar")
    const mobileOverlay = document.getElementById("mobileOverlay")

    if (menuToggle) {
      menuToggle.addEventListener("click", () => this.toggleMobileMenu())
    }

    if (mobileOverlay) {
      mobileOverlay.addEventListener("click", () => this.closeMobileMenu())
    }

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && sidebar && sidebar.classList.contains("open")) {
        this.closeMobileMenu()
      }
    })
  }

  setupThemeToggle() {
    const themeToggle = document.getElementById("themeToggle")
    if (themeToggle) {
      themeToggle.addEventListener("click", () => this.toggleTheme())
    }
  }

  setupNavigation() {
    const navLinks = document.querySelectorAll(".nav-item a")
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        this.closeMobileMenu()
      })
    })

    const footerLinks = document.querySelectorAll(".footer-links a")
    footerLinks.forEach((link) => {
      const href = link.getAttribute("href")
      if (!href || href === "#") {
        link.addEventListener("click", (e) => {
          e.preventDefault()
          const linkText = link.textContent.trim()
          this.showToast(`${linkText} - Coming Soon!`)
        })
      }
    })
  }

  toggleMobileMenu() {
    const menuToggle = document.getElementById("menuToggle")
    const sidebar = document.getElementById("sidebar")
    const mobileOverlay = document.getElementById("mobileOverlay")

    if (!menuToggle || !sidebar || !mobileOverlay) return

    menuToggle.classList.toggle("active")
    sidebar.classList.toggle("open")
    mobileOverlay.classList.toggle("active")

    document.body.style.overflow = sidebar.classList.contains("open") ? "hidden" : ""
  }

  closeMobileMenu() {
    const menuToggle = document.getElementById("menuToggle")
    const sidebar = document.getElementById("sidebar")
    const mobileOverlay = document.getElementById("mobileOverlay")

    if (menuToggle) menuToggle.classList.remove("active")
    if (sidebar) sidebar.classList.remove("open")
    if (mobileOverlay) mobileOverlay.classList.remove("active")

    document.body.style.overflow = ""
  }

  showToast(message) {
    let toast = document.querySelector(".toast-notification")

    if (!toast) {
      toast = document.createElement("div")
      toast.className = "toast-notification"
      document.body.appendChild(toast)

      toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: var(--accent-color);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        transform: translateY(100px);
        transition: transform 0.3s ease;
        max-width: 300px;
        font-size: 0.9rem;
        font-weight: 500;
      `
    }

    toast.textContent = message

    setTimeout(() => {
      toast.style.transform = "translateY(0)"
    }, 100)

    clearTimeout(this.toastTimeout)
    this.toastTimeout = setTimeout(() => {
      toast.style.transform = "translateY(100px)"
    }, 3000)
  }

  addInteractiveEffects() {
    const actionButtons = document.querySelectorAll(".resource-btn")

    actionButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        const ripple = document.createElement("span")
        const rect = button.getBoundingClientRect()
        const size = Math.max(rect.width, rect.height)
        const x = e.clientX - rect.left - size / 2
        const y = e.clientY - rect.top - size / 2

        ripple.style.cssText = `
          position: absolute;
          width: ${size}px;
          height: ${size}px;
          left: ${x}px;
          top: ${y}px;
          background: rgba(255, 255, 255, 0.3);
          border-radius: 50%;
          transform: scale(0);
          animation: ripple 0.6s linear;
          pointer-events: none;
        `

        button.style.position = "relative"
        button.style.overflow = "hidden"
        button.appendChild(ripple)

        setTimeout(() => {
          ripple.remove()
        }, 600)
      })
    })

    if (!document.getElementById("ripple-style")) {
      const style = document.createElement("style")
      style.id = "ripple-style"
      style.textContent = `
        @keyframes ripple {
          to {
            transform: scale(4);
            opacity: 0;
          }
        }
      `
      document.head.appendChild(style)
    }
  }
}

function showComingSoon(feature) {
  const dashboard = window.teacherDashboard
  if (dashboard) {
    dashboard.showToast(`${feature} - Coming Soon!`)
  } else {
    alert(`${feature} - Coming Soon!`)
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.teacherDashboard = new TeacherDashboard()
})

document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll('img[src*="placeholder"]')

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target
        observer.unobserve(img)
      }
    })
  })

  images.forEach((img) => imageObserver.observe(img))
})

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
  const savedTheme = localStorage.getItem("dashboard-theme")
  if (!savedTheme) {
    const newTheme = e.matches ? "dark" : "light"
    document.documentElement.setAttribute("data-theme", newTheme)
    localStorage.setItem("dashboard-theme", newTheme)
  }
})