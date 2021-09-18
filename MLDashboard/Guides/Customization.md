# Customization

Dashboards are created based on .json config files.

These files look like this:
```python
{
    "modules": [
        [
            ["LossMetricsGraph", {}],
            ["LossMetricsNumerical", {}]
        ],
        [
            ["StatusModule",{}],
            ["EmptyModule", {}]
        ]
    ]
}
```

This will create a dashboard that looks like this.

| Loss Metrics Graph | Loss Metrics Numerical |
|:------------------:|:----------------------:|
|  __Status Module__ |    __Empty Module__    |

More modules can easily be added, as long as they form a grid.

Modules should be referred to by their "friendly name" as defined in this code:
```python
{'LossMetricsGraph': LossMetricsGraph,
 'LossMetricsNumerical': LossMetricsNumerical,
 'StatusModule': StatusModule,
 'ControlButtons': ControlButtons,
 'TrainingSetSampleImages': TrainingSetSampleImages,
 'PredImages': PredImages,
 'WrongPredImages': WrongPredImages,
 'EmptyModule': EmptyModule}
```

Modules can have configuration. This is added in the {} after the module name.

```python
["TrainingSetSampleImages", {"width": 28, "height": 28, "rows": 2, "cols": 4, "refreshrate": 5}]
```

Configuration can also be passed to all modules by adding it into the main json.

```python
{
    "modules":[
        [
          ["TrainingSetSampleImages",{}],
          ["WrongPredImages", {}]
        ],
    ],
    "config": {
        "width": 28,
        "height": 28,
        "rows": 2,
        "cols": 4,
        "correctcolor": "blue",
        "incorrectcolor": "orange",
        "refreshrate": 5
    }
  }
}
```

Modules will ignore config that they don't need.

More info on configuration can be found in the module documentation.