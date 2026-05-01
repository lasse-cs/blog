import "../css/blog.css";

import { Application } from "@hotwired/stimulus"

import NavController from "./controllers/nav_controller.js";
import ThemeController from "./controllers/theme_controller.js";
import ActivityController from "./controllers/activity_controller.js"
import ClipboardController from "./controllers/clipboard_controller.js"

const application = Application.start()
application.register("nav", NavController);
application.register("theme", ThemeController);
application.register("activity", ActivityController);
application.register("clipboard", ClipboardController);