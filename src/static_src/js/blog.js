import { Application } from "@hotwired/stimulus"

import NavController from "@/controllers/nav_controller"
import ThemeController from "@/controllers/theme_controller"

window.Stimulus = Application.start()
Stimulus.register("nav", NavController);
Stimulus.register("theme", ThemeController);