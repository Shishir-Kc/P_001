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
    this.ensureThemeLoaded()
    this.addInteractiveEffects()
  }

  ensureThemeLoaded() {
    // Double-check theme is properly loaded
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

    // Add a subtle animation effect
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

    // Close menu on escape key
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
    // Only handle mobile menu closing for navigation links
    const navLinks = document.querySelectorAll(".nav-item a")

    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        // Just close mobile menu and let the browser handle navigation normally
        this.closeMobileMenu()
      })
    })

    // Handle footer links separately for special cases
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

    if (!menuToggle || !sidebar || !mobileOverlay) {
      console.error("Mobile menu elements not found")
      return
    }

    menuToggle.classList.toggle("active")
    sidebar.classList.toggle("open")
    mobileOverlay.classList.toggle("active")

    // Prevent body scroll when menu is open
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
    // Create toast element if it doesn't exist
    let toast = document.querySelector(".toast-notification")

    if (!toast) {
      toast = document.createElement("div")
      toast.className = "toast-notification"
      document.body.appendChild(toast)

      // Add toast styles
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

    // Update message
    toast.textContent = message

    // Show toast
    setTimeout(() => {
      toast.style.transform = "translateY(0)"
    }, 100)

    // Hide after delay
    clearTimeout(this.toastTimeout)
    this.toastTimeout = setTimeout(() => {
      toast.style.transform = "translateY(100px)"
    }, 3000)
  }

  addInteractiveEffects() {
    // Add hover effects to action buttons
    const actionButtons = document.querySelectorAll(".resource-btn")

    actionButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        // Create ripple effect
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

    // Add CSS for ripple animation
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

// Global function for coming soon features
function showComingSoon(feature) {
  const dashboard = window.teacherDashboard
  if (dashboard) {
    dashboard.showToast(`${feature} - Coming Soon!`)
  } else {
    alert(`${feature} - Coming Soon!`)
  }
}

// Initialize the dashboard when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.teacherDashboard = new TeacherDashboard()
})

// Performance optimization: Lazy load images
document.addEventListener("DOMContentLoaded", () => {
  const images = document.querySelectorAll('img[src*="placeholder"]')

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target
        // In a real app, you would load the actual image here
        observer.unobserve(img)
      }
    })
  })

  images.forEach((img) => imageObserver.observe(img))
})

// Handle system theme changes and update saved preference
window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
  const savedTheme = localStorage.getItem("dashboard-theme")
  // Only update if user hasn't manually set a preference
  if (!savedTheme) {
    const newTheme = e.matches ? "dark" : "light"
    document.documentElement.setAttribute("data-theme", newTheme)
    localStorage.setItem("dashboard-theme", newTheme)
  }
})
