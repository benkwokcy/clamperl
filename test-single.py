import json
import test

from app import logic, structures

mock = test.formatJson('{"Turn":76,"Food":[{"X":4,"Y":5}],"Snakes":[{"ID":"gs_XJT4cMq4GGH83txHxFh8ybDC","Name":"1obo / S-1000","URL":"","Body":[{"X":10,"Y":4},{"X":10,"Y":3},{"X":9,"Y":3},{"X":8,"Y":3},{"X":7,"Y":3},{"X":6,"Y":3}],"Health":99,"Death":null,"Color":"#000000","HeadType":"tongue","TailType":"freckled","Latency":"39","Shout":""},{"ID":"gs_qB8JGSXX46x7yVJ8Xq4hXQ8R","Name":"benkwokcy / huntail","URL":"","Body":[{"X":8,"Y":6},{"X":8,"Y":7},{"X":9,"Y":7},{"X":10,"Y":7},{"X":10,"Y":8}],"Health":62,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"90","Shout":""},{"ID":"gs_WqcBpXhK97DgWW3JpfbWrtmQ","Name":"synthesizedsoul / D.Va","URL":"","Body":[{"X":3,"Y":5},{"X":3,"Y":6},{"X":4,"Y":6},{"X":4,"Y":7},{"X":4,"Y":8},{"X":3,"Y":8},{"X":2,"Y":8},{"X":2,"Y":9},{"X":3,"Y":9},{"X":3,"Y":10},{"X":2,"Y":10}],"Health":95,"Death":null,"Color":"#EE4BB5","HeadType":"","TailType":"","Latency":"116","Shout":""},{"ID":"gs_qQPjpjHtbp8h9SSVfMxVGxh8","Name":"sockbot / fearless-snake","URL":"","Body":[{"X":4,"Y":4},{"X":5,"Y":4},{"X":5,"Y":5},{"X":6,"Y":5},{"X":6,"Y":6},{"X":6,"Y":7},{"X":6,"Y":8},{"X":6,"Y":9},{"X":6,"Y":10}],"Health":91,"Death":null,"Color":"#EC86AC","HeadType":"","TailType":"","Latency":"85","Shout":""}]}')
logic.getMove(mock)
