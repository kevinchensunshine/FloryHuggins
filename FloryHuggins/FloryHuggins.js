
var NA = 100;
var NB = 100;
var chi = 0.02;
//var tangent = [NaN, NaN, NaN, NaN]
//var spinodal = [NaN, NaN, NaN, NaN]

function createObject(object, variableName){
  //Bind a variable whose name is the string variableName
  // to the object called 'object'
  let execString = variableName + " = object"
  //console.log("Running `" + execString + "`");
  eval(execString)
}

function handle_na() {
    const slider = document.getElementById("NA");
    NA = parseFloat(slider.value);
    document.getElementById("value_of_NA").innerHTML = NA.toString();
    draw()
    update_tangent_and_spinodal()
}

function handle_nb() {
    const slider = document.getElementById("NB");
    NB = parseFloat(slider.value);
    document.getElementById("value_of_NB").innerHTML = NB.toString();
    draw()
    update_tangent_and_spinodal()
}

// Update the current slider value (each time you drag the slider handle)
function handle_chi() {
    const slider = document.getElementById("chi");
    chi = parseFloat(slider.value);
    document.getElementById("value_of_chi").innerHTML = chi.toString();
    draw()
    update_tangent_and_spinodal()
}

async function update_tangent_and_spinodal() {
  tangent = pyodideGlobals.get('tangent').toJs()
  spinodal = pyodideGlobals.get('spinodal').toJs()
  draw_flory_huggins(NA, NB, chi, "tangent_and_binodal", tangent, spinodal)
  console.log("tangent", tangent)
  console.log("spinodal", spinodal)
}

function draw() {
    draw_flory_huggins(NA, NB, chi, "floryhuggins", [NaN, NaN, NaN, NaN], [NaN, NaN, NaN, NaN]);
}

function F_mix(phi,NA,NB,chi,kT) {
    return kT*(chi*phi*(1.0-phi) + phi/NA*Math.log(phi) + (1.0-phi)/NB*Math.log(1.0-phi))
}

function draw_flory_huggins(na, nb, c, canvas_id, tangent, binodal) {
    const canvas = document.getElementById(canvas_id);
    if (canvas.getContext) {
      
      // pre-calculate fixed number of points on the curve so that we can estimate the
      // range of y values (Delta F mix)
      const number_of_points_to_plot = 100;

      let x_values = Array(number_of_points_to_plot + 1);
      let y_values = Array(number_of_points_to_plot + 1);

      const x_min = 0.001;
      const x_max = 0.999;
      const x_range = x_max - x_min;

      for (let i = 0; i <= number_of_points_to_plot; i++)
      {
        x_values[i] = x_min + i * x_range / number_of_points_to_plot;
        y_values[i] = F_mix(x_values[i], na, nb, c, 1.0);
      }

      const y_min = Math.min(...y_values);
      const y_max = Math.max(...y_values);
      const y_range = y_max - y_min;

      // get canvas drawuing context
      const ctx = canvas.getContext('2d');

      // set/calculate margins on all sides, the curve will be drawn inside
      // a rectange so there are two sets of margins: one set for the rectangle
      // and one set for the curve inside the rectangle
      const left_of_rectangle = 100;  // enough space on left side for y-axis label
      const top_of_rectangle = 10;
      const width_of_rectangle = canvas.width - left_of_rectangle - 5;
      const height_of_rectangle = canvas.height - top_of_rectangle - 50; // enough space on bottom for x-axis label

      const left_margin = left_of_rectangle + 10;
      const right_margin = canvas.width - left_of_rectangle - width_of_rectangle + 10;
      const top_margin = top_of_rectangle + 10;
      const bottom_margin = canvas.height - top_of_rectangle - height_of_rectangle + 10;
      const horizontal_margins = left_margin + right_margin;
      const vertical_margins = top_margin + bottom_margin;

      // calculate scaling factors to draw the curve on the canvas
      const scale_x = (canvas.width - horizontal_margins) / x_range;
      const scale_y = (canvas.height - vertical_margins) / y_range;

      // offsets to add to the coordinates to draw the curve at right place
      // relative to left and top margins
      const offset_x = left_margin - x_min * scale_x;
      const offset_y = top_margin + y_max * scale_y;

      // calculate the canvas coordinates of the first point
      const first_point_x = offset_x + x_values[0] * scale_x;
      const first_point_y = offset_y - y_values[0] * scale_y;

      // clear everything in the canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // draw the rectangle
      ctx.lineWidth = 1;
      ctx.strokeStyle = "black";
      ctx.strokeRect(left_of_rectangle, top_of_rectangle, width_of_rectangle, height_of_rectangle);

      // constants for horizontal tick marks
      const x_tick_min = 0.0;
      const x_tick_max = 1.0;
      const x_tick_step = 0.2;
      const number_of_x_ticks = (x_tick_max - x_tick_min) / x_tick_step + 1;

      ctx.textAlign = "center";

      const bottom_of_rectangle = top_of_rectangle + height_of_rectangle;

      // draw horizontal tick marks
      for (let i = 0; i < number_of_x_ticks; i++)
      {
        ctx.beginPath();
        const tick_value = x_tick_min + x_tick_step * i;
        const tick_mark_x = offset_x + tick_value * scale_x;
        ctx.moveTo(tick_mark_x, bottom_of_rectangle);
        ctx.lineTo(tick_mark_x, bottom_of_rectangle + 5);
        ctx.stroke();
        // draw the scale value for this tick mark
        ctx.fillText(tick_value.toFixed(1).toString(), tick_mark_x, bottom_of_rectangle + 15);
      }

      // label the x-axis
      ctx.fillText("\u03d5", left_of_rectangle + width_of_rectangle / 2, bottom_of_rectangle + 30);

      // calculate tick min/max/step on the vertical direction
      const y_range_2_significant_digits = y_range.toPrecision(2);
      const number_of_digits_after_decimal_point = y_range_2_significant_digits.length - y_range_2_significant_digits.indexOf(".") - 1;
      const scaling_factor_for_rounding = 10 ** number_of_digits_after_decimal_point;
      const y_tick_min = Math.floor(y_min * scaling_factor_for_rounding) / scaling_factor_for_rounding;
      const y_tick_max = Math.ceil(y_max * scaling_factor_for_rounding) / scaling_factor_for_rounding;
      const number_of_y_ticks = 6;
      const y_tick_step = (y_tick_max - y_tick_min) / (number_of_y_ticks - 1);

      ctx.textAlign = "right";
      ctx.textBaseline = "middle";

      // draw vertical tick marks
      for (let i = 0; i < number_of_y_ticks; i++)
      {
        ctx.beginPath();
        const tick_value = y_tick_min + y_tick_step * i;
        const tick_mark_y = offset_y - tick_value * scale_y;
        ctx.moveTo(left_of_rectangle, tick_mark_y);
        ctx.lineTo(left_of_rectangle - 5, tick_mark_y);
        ctx.stroke();
        // draw the scale value for this tick mark
        ctx.fillText(tick_value.toFixed(number_of_digits_after_decimal_point).toString(), left_of_rectangle - 10, tick_mark_y);
      }

      // lable the y-axis
      ctx.textAlign = "left";
      ctx.fillText("\u0394F_mix", 5, top_of_rectangle + height_of_rectangle / 2);

      // finally draw the Flory Huggins curve
      ctx.beginPath();
      ctx.moveTo(first_point_x, first_point_y);
      for (let i = 1; i <= number_of_points_to_plot; i++)
      {
        ctx.lineTo(offset_x + x_values[i] * scale_x, offset_y - y_values[i] * scale_y);
      }
      ctx.lineWidth = 1;
      ctx.strokeStyle = "blue";
      ctx.stroke();

      // draw tangent line
      if (!isNaN(tangent[0]))
      {
        draw_red_line(offset_x + tangent[0] * scale_x, offset_y - tangent[2] * scale_y,
        offset_x + tangent[1] * scale_x, offset_y - tangent[3] * scale_y, ctx);
      }

      // draw binodal points
      if (!isNaN(binodal[0]))
      {
        draw_green_dot(offset_x + binodal[0] * scale_x, offset_y - binodal[2] * scale_y, ctx);
        draw_green_dot(offset_x + binodal[1] * scale_x, offset_y - binodal[3] * scale_y, ctx);
      }
    }
}

function draw_green_dot(x, y, context)
{
  const save = context.fillStyle;

  context.beginPath();
  context.arc(x, y, 3, 0, 2 * Math.PI);
  context.fillStyle = "green";
  context.fill();
  context.fillStyle = save;
}

function draw_red_line(x1, y1, x2, y2, context)
{
  context.beginPath();
  context.moveTo(x1, y1);
  context.lineTo(x2, y2);
  context.setLineDash([10, 5]);
  const save = context.strokeStyle;
  context.strokeStyle = "red";
  context.stroke();
  context.setLineDash([]);
  context.strokeStyle = save;
}