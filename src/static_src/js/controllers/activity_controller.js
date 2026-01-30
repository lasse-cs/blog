import { Controller } from "@hotwired/stimulus"
import * as d3 from "d3";

export default class extends Controller {
    static targets = [ "svgContainer" ]

    connect() {
        const dataScript = this.element.querySelector('script[type="application/json"]');
        if (!dataScript) {
            return;
        }

        const data = JSON.parse(dataScript.textContent);
        data.forEach(element => {
            element.activity_date = new Date(element.activity_date)
        });
        data.sort((a, b) => a.activity_date - b.activity_date);

        const activityExtent = [1, d3.max(data.map(d => d.activities))];

        const activityScale = d3.scaleQuantize()
            .domain(activityExtent)
            .range(["very-low", "low", "medium", "high", "very-high"]);

        const getActivityIndicator = (activities) => {
            if (activities === 0) {
                return "none";
            } else {
                return activityScale(activities);
            }
        }

        const xScale = d3.scaleBand()
            .domain(data.map(d => d.activity_date))
            .range([2, 225])
            .paddingInner(0.2);

        const days = ["S", "M", "T", "W", "T", "F", "S"];
        const squareSize = xScale.bandwidth();

        const svg = d3.select(this.svgContainerTarget)
            .append("svg")
            .attr("viewBox", "0 0 240 80");

        const boxAndLabel = svg
            .selectAll("g")
            .data(data)
            .join("g")
            .attr("transform", d => `translate(${xScale(d.activity_date)}, 5)`);

        boxAndLabel
            .append("rect")
            .attr("class", "day-box")
            .attr("width", squareSize)
            .attr("height", squareSize)
            .attr("rx", 5)
            .attr("ry", 5)
            .attr("class", d => `day__box ${getActivityIndicator(d.activities)}`);

        boxAndLabel
            .append("text")
            .text(d => days[d.activity_date.getDay()])
            .attr("y", squareSize + 20)
            .attr("x", squareSize / 2 - 7)
            .attr("class", "day__label");

        boxAndLabel
            .append("title")
            .text(d => `${d.activity_date.toDateString()}: ${d.activities}`);
    }
}
