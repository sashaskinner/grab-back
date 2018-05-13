  // populate map with data showing % women employed overall by district
  function womenEmployeesData() {
  
    //draw chartjs chart
    $("#district-rank").remove();
    $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
    var ctx = $("#district-rank");
    createRankChartEmployee();
    
    var minimum = 0.33,
        maximum = 0.52;
      queue()
      .defer(d3.json, "/us.json")
      .defer(d3.json, "/us-congress-113.json")
      .defer(d3.json, "/district-employee-info.json")
      .await(ready);
  } // end womenEmployeesData
  function womenEmployeesDataReverse() {
  
    //draw chartjs chart
    $("#district-rank").remove();
    $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
    var ctx = $("#district-rank");
    createReverseChartEmployee();
    
    var minimum = 0.33,
        maximum = 0.52;
      queue()
      .defer(d3.json, "/us.json")
      .defer(d3.json, "/us-congress-113.json")
      .defer(d3.json, "/district-employee-info.json")
      .await(ready);
  } // end womenEmployeesData
  // populate map with data showing % women employed in management positions by district
  function womenManagersData() {
        
        // draw chartjs chart
        $("#district-rank").remove();
        $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
        var ctx = $("#district-rank")
        createRankChartManager();
        var minimum = 0.28,
            maximum = 0.62;
        queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-manager-info.json")
        .await(ready);
  } // end womenManagersData
  function womenManagersDataReverse() {
        // draw chartjs chart
        $("#district-rank").remove();
        $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
        var ctx = $("#district-rank")
        createReverseChartManager();
        var minimum = 0.28,
            maximum = 0.62;
        queue()
        .defer(d3.json, "/us.json")
        .defer(d3.json, "/us-congress-113.json")
        .defer(d3.json, "/district-manager-info.json")
        .await(ready);
        // debugger
  } // end womenManagersData
  // create bar chart
  function createRankChartEmployee() {
      
      $("#district-rank").remove();
      $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
      
      var ctx = $("#district-rank");
      var yearValue = $("#year").val();
      
      $.get("/chart-data-employee?year="+yearValue, function (results) {
        var data = {
          labels: results[0],
          datasets: [
          {
            data: results[1],
            backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
          }]
        };
        var districtRankChart = new Chart(ctx, {
          type: 'horizontalBar',
          data: data,
          options: {
              responsive: false,
              title: {
                  display: true,
                  text: 'Districts With Highest % Female Employees'},
              legend: {
                  display: false
              }
                }}
              );
      })
    };
  function createReverseChartEmployee() {
      
      $("#district-rank").remove();
      $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
      var ctx = $("#district-rank");
      var yearValue = $("#year").val();
      
      $.get("/chart-data-employee-reverse?year="+yearValue, function (results) {
        var data = {
          labels: results[0],
          datasets: [
          {
            data: results[1],
            backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]            
          }]
        };
        var districtRankChart = new Chart(ctx, {
          type: 'horizontalBar',
          data: data,
          options: {
              responsive: false,
              title: {
                  display: true,
                  text: 'Districts With Lowest % Female Employees'},
              legend: {
                  display: false
              }
              }
              });
      });
    }

  function createRankChartManager() {
      
      $("#district-rank").remove();
      $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
      var ctx = $("#district-rank");
      var yearValue = $("#year").val();
      
      $.get("/chart-data-manager?year="+yearValue, function (results) {
        var data = {
          labels: results[0],
          datasets: [
          {
            data: results[1],
            backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
          }]
        };
        var districtRankChart = new Chart(ctx, {
          type: 'horizontalBar',
          data: data,
          options: {
              responsive: false,
              title: {
                  display: true,
                  text: 'Districts With Highest % Female Employees in Management'
                },
              legend: {
                  display: false
              }}
              });
      });
    }
  
  function createReverseChartManager() {
      
      $("#district-rank").remove();
      $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
      var ctx = $("#district-rank");
      var yearValue = $("#year").val();
      $.get("/chart-data-manager-reverse?year="+yearValue, function (results) {
        var data = {
          labels: results[0],
          datasets: [
          {
            data: results[1],
            backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
          }]
        };
        var districtRankChart = new Chart(ctx, {
          type: 'horizontalBar',
          data: data,
          options: {
              responsive: false,
              title: {
                  display: true,
                  text: 'Districts With Lowest % Female Employees in Management'
                },
               legend: {
                  display: false
              }}
              });
      });
    }

    // change data based on button click
    ////////////////////////////////////
    // all employees button selected ///
    
    $("#allEmp").on("change", function () {
              
              var yearValue = $("#year").val();
              var zipcode = $("#zipcode-entry").val();
              var zipOnly = $("#view-zip-compare").is(":checked");
              queue()
              .defer(d3.json, "/us.json")
              .defer(d3.json, "/us-congress-113.json")
              .defer(d3.json, "/district-employee-info.json?year="+yearValue)
              .await(ready);
        if ( zipOnly === false ) {
              $("#district-rank").remove();
              $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
              
              var ctx = $("#district-rank");
                
                $.get("/chart-data-employee?year="+yearValue,
                  function (results) {
                      var data = {
                        labels: results[0],
                        datasets: [
                        {
                          data: results[1],
                          backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
                        }]
                  };
                  var districtRankChart = new Chart(ctx, {
                    type: 'horizontalBar',
                    data: data,
                    options: {
                        responsive: false,
                        title: {
                            display: true,
                            text: 'Districts With Highest % Female Employees'},
                        legend: {
                            display: false
                        }
                          }}
                        );
                }); } // end if statement
       else if ( zipOnly === true ) {
          
          $.get("/zipcode-lookup.json?year="+yearValue, { "zipcode-entry":zipcode }, ZipcodeLookup);
       } //end else if 
        });
    
    $("#manager").on("change", function () {
        var yearValue = $("#year").val();
        var zipcode = $("#zipcode-entry").val();
        
        var zipOnly = $("#view-zip-compare").is(":checked");
        queue()
              .defer(d3.json, "/us.json")
              .defer(d3.json, "/us-congress-113.json")
              .defer(d3.json, "/district-manager-info.json?year="+yearValue)
              .await(ready);
        
        if ( zipOnly === false ) {

          function updateRankChartManager() {
            $("#district-rank").remove();
            $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
            
            createRankChartManager();
            }
          updateRankChartManager();
       } // end if statement
       else if ( zipOnly === true ) {
          
          $.get("/zipcode-lookup.json?year="+yearValue, { "zipcode-entry":zipcode }, ZipcodeLookup);
       } //end else if 
      } // end anonymous function for on manager click.
      );
      
      // bottom five employee districts selected 
      $("#bottomFiveEmp").on("change", function () {
          
          $("#district-rank").remove();
          $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
          
          var ctx = $("#district-rank");
          var yearValue = $("#year").val();
          $.get("/chart-data-employee-reverse?year="+yearValue, function (results) {
            var data = {
              labels: results[0],
              datasets: [
              {
                data: results[1],
                backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
              }]
            };
            var districtRankChart = new Chart(ctx, {
              type: 'horizontalBar',
              data: data,
              options: {
                  responsive: false,
                  title: {
                      display: true,
                      text: 'Districts With Lowest % Female Employees'},
                  legend: {
                      display: false
                  }
                  }
                  });
          });
        }); // end updateReverseChartEmployee
      // bottom five manager districts selected
        $("#bottomFiveManager").on("change", function () {
        // draw chartjs chart
        $("#district-rank").remove();
        $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
        
        var ctx = $("#district-rank");
        var yearValue = $("#year").val();
        $.get("/chart-data-manager-reverse?year="+yearValue, function (results) {
            var data = {
              labels: results[0],
              datasets: [
              {
                data: results[1],
                backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
              }]
            };
            var districtRankChart = new Chart(ctx, {
              type: 'horizontalBar',
              data: data,
              options: {
                  responsive: false,
                  title: {
                      display: true,
                      text: 'Districts With Lowest % Female Employees in Management'
                    },
                   legend: {
                      display: false
                  }}
                  });
      });
      });
    //////////////////////
    // was the slider used?
    $("#year").on("input", function () {
        var yearValue = $("#year").val();
        var zipcode = $("#zipcode-entry").val();
        var zipOnly = $("#view-zip-compare").is(":checked");
        $("#currentYear").text("Percent women employed in " + yearValue);
        $("#sliderYear").text(yearValue);
        if (zipOnly === true && $('input[name=empType]:checked', '#category').val() === "allEmps") {
        
          $.get("/zipcode-lookup.json?year="+yearValue, {"zipcode-entry":zipcode}, ZipcodeLookup);
        } // end if statement
        else if (zipOnly === true && $('input[name=empType]:checked', '#category').val() === "Managers") {
          $.get("/zipcode-lookup.json?year="+yearValue, {"zipcode-entry":zipcode}, ZipcodeLookup);
      } // end else if statement
        else if ($('input[name=empType]:checked', '#category').val() === "Managers") {
  
        queue()
              .defer(d3.json, "/us.json")
              .defer(d3.json, "/us-congress-113.json")
              .defer(d3.json, "/district-manager-info.json?year="+yearValue)
              .await(ready);
        
        function updateRankChartManager() {
          $("#district-rank").remove();
          $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
          
          createRankChartManager();
          }
        updateRankChartManager();
      } // end if statement (if radio button "manager is checked")
      else if ($('input[name=empType]:checked', '#category').val() === "allEmps") {
        
        queue()
              .defer(d3.json, "/us.json")
              .defer(d3.json, "/us-congress-113.json")
              .defer(d3.json, "/district-employee-info.json?year="+yearValue)
              .await(ready);
        function updateRankChartEmployee() {
          $("#district-rank").remove();
          $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
          
          var ctx = $("#district-rank");
            
            $.get("/chart-data-employee?year="+yearValue,
              function (results) {
                  var data = {
                    labels: results[0],
                    datasets: [
                    {
                      data: results[1],
                      backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
                    }]
              };
              var districtRankChart = new Chart(ctx, {
                type: 'horizontalBar',
                data: data,
                options: {
                    responsive: false,
                    title: {
                        display: true,
                        text: 'Districts With Highest % Female Employees'},
                    legend: {
                        display: false
                    }
                      }}
                    );
            });
      }
        updateRankChartEmployee();
    }
    
    else if ($("input[type=radio][id=bottomFiveEmp]:checked").val() == "on") {
      function updateReverseChartEmployee() {
          
          $("#district-rank").remove();
          $("#graph-container").append("<canvas id='district-rank' width=450, height=400></canvas>");
          
          var ctx = $("#district-rank");
          var yearValue = $("#year").val();
          $.get("/chart-data-employee-reverse?year="+yearValue, function (results) {
            var data = {
              labels: results[0],
              datasets: [
              {
                data: results[1],
                backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
              }]
            };
            var districtRankChart = new Chart(ctx, {
              type: 'horizontalBar',
              data: data,
              options: {
                  responsive: false,
                  title: {
                      display: true,
                      text: 'Districts With Lowest % Female Employees in Management'
                    },
                   legend: {
                      display: false
                  }}
                  });
          });
          } // end updateReverseChartEmployee
          updateReverseChartEmployee();
        } // end else if radio button checked is bottomFiveEmp
    else if ($("input[type=radio][id=bottomFiveManager]:checked").val() == "on") {
      function updateReverseChartManager() {
        // draw chartjs chart
        $("#district-rank").remove();
        $("#graph-container").append("<canvas id='district-rank' width=450, height=400</canvas>");
        
        var ctx = $("#district-rank");
        $.get("/chart-data-manager-reverse?year="+yearValue, function (results) {
            var data = {
              labels: results[0],
              datasets: [
              {
                data: results[1],
                backgroundColor: ["#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#2f78c4", "#084081"]
              }]
            };
            var districtRankChart = new Chart(ctx, {
              type: 'horizontalBar',
              data: data,
              options: {
                  responsive: false,
                  title: {
                      display: true,
                      text: 'Districts With Lowest % Female Employees in Management'
                    },
                   legend: {
                      display: false
                  }}
                  });
      });
      } // end updateReverseChartManager
      updateReverseChartManager();
      } // end else if radio butoon checked is bottomFiveManager
    });