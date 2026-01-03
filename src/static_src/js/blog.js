import "@/css/blog.css"

import { Application } from "@hotwired/stimulus"

import NavController from "@/js/controllers/nav_controller"
import ThemeController from "@/js/controllers/theme_controller"

window.Stimulus = Application.start()
Stimulus.register("nav", NavController);
Stimulus.register("theme", ThemeController);