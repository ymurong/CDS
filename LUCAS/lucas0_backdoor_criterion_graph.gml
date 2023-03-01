graph [
  directed 1
  node [
    id 0
    label "Smoking"
  ]
  node [
    id 1
    label "Yellow_Fingers"
  ]
  node [
    id 2
    label "Anxiety"
  ]
  node [
    id 3
    label "Peer_Pressure"
  ]
  node [
    id 4
    label "Genetics"
  ]
  node [
    id 5
    label "Attention_Disorder"
  ]
  node [
    id 6
    label "Born_an_Even_Day"
  ]
  node [
    id 7
    label "Car_Accident"
  ]
  node [
    id 8
    label "Fatigue"
  ]
  node [
    id 9
    label "Allergy"
  ]
  node [
    id 10
    label "Coughing"
  ]
  node [
    id 11
    label "Lung_cancer"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 0
    target 11
  ]
  edge [
    source 2
    target 0
  ]
  edge [
    source 3
    target 0
  ]
  edge [
    source 4
    target 5
  ]
  edge [
    source 4
    target 11
  ]
  edge [
    source 5
    target 7
  ]
  edge [
    source 8
    target 7
  ]
  edge [
    source 9
    target 10
  ]
  edge [
    source 10
    target 8
  ]
  edge [
    source 11
    target 10
  ]
]
