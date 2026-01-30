import "@/css/blog.css"

import { Application } from "@hotwired/stimulus"

import NavController from "@/js/controllers/nav_controller"
import ThemeController from "@/js/controllers/theme_controller"
import ActivityController from "@/js/controllers/activity_controller"

window.Stimulus = Application.start()
Stimulus.register("nav", NavController);
Stimulus.register("theme", ThemeController);
Stimulus.register("activity", ActivityController);