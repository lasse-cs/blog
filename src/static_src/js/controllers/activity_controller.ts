import { Controller } from "@hotwired/stimulus"
import * as d3 from "d3";

type ActivityByDayJson = {
    activity_date: string;
    activities: number;
}

type ActivityByDay = {
    activity_date: Date;
    activities: number;
}

export default class extends Controller {
    static targets = [ "svgContainer" ]

    declare readonly svgContainerTarget: HTMLElement;

    connect() {
        const dataScript = this.element.querySelector('script[type="application/json"]');
        if (!dataScript) {
            return;
        }

        const rawData: ActivityByDayJson[] = JSON.parse(dataScript.textContent);
        const data: ActivityByDay[] = rawData.map(({ activity_date, activities }) => ({
            activity_date: new Date(activity_date), activities: activities
        }));
        data.sort((a, b) => a.activity_date.getTime() - b.activity_date.getTime());

        const activityExtent = [1, d3.max(data.map(d => d.activities)) ?? 1];

        const activityScale = d3.scaleQuantize<string>()
            .domain(activityExtent)
            .range(["very-low", "low", "medium", "high", "very-high"]);

        const getActivityIndicator = (activities: number) => {
            if (activities === 0) {
                return "none";
            } else {
                return activityScale(activities);
            }
        }

        const xScale = d3.scaleBand<Date>()
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
