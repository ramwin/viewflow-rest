# viewflow-rest
provide restful viewflow 

many of code in the project looks like django-viewflow. I want to keep the interface as same as the [django viewflow](https://github.com/viewflow/viewflow).

Thanks you for all the [contributors of viewflow](https://github.com/viewflow/viewflow/graphs/contributors).

**The project is under GPL-3.0 License, any one who change the source code (even if you just use it in intranet of just at home) should upload his code**


# workflow
A flow contains many nodes  
every node is a instance of Node
every node have a `activation_class`  
every `action_class` instance will `activate_next` by
```
self.flow_task._next  // the next node instance
self.flow_task._next.activate // 
```

# 依赖顺序

## Edge
* src: source Node instance
* dst: target Node instance

## activations
* Attribute
    * `flow_class`
    * `flow_task`: Node Instance defined in the `flows.py`
    * `task`: Current Task

## Nodes
* Function
    * `_incoming`: Edge Instance list
    * `_outgoing`: Edge Instance list

3. models

4. Views

6. Flow


9. rest_extensions

