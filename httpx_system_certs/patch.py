from functools import wraps
import ssl
import truststore
import httpx
import inspect

def patch():
    def change_function_default_ssl_context(func, ssl_context_arg='verify'):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if ssl_context_arg not in kwargs.keys():
                ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                kwargs[ssl_context_arg] = ssl_context
            return func(*args, **kwargs)
        
        return wrapper
        
    def change_class_default_ssl_context(cls, ssl_context_arg='verify'):
        init = cls.__init__

        @wraps(init)
        def wrapper(self, *args, **kwargs):
            if ssl_context_arg not in kwargs.keys():
                ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                kwargs[ssl_context_arg] = ssl_context
            return init(self, *args, **kwargs)
        
        cls.__init__ = wrapper
        return cls
    
    for name, obj in inspect.getmembers(httpx):
        if inspect.isclass(obj):
            for param in inspect.signature(obj.__init__).parameters.values(): 
                    if str(param.annotation).find('ssl.SSLContext') !=  -1: change_class_default_ssl_context(obj, ssl_context_arg=param.name)
        elif inspect.isfunction(obj):
            for param in inspect.signature(obj).parameters.values(): 
                if str(param.annotation).find('ssl.SSLContext') !=  -1: 
                    patched = change_function_default_ssl_context(obj, ssl_context_arg=param.name)
                    setattr(httpx, name, patched)

if __name__ == "__main__":
    names = []
    for name, obj in inspect.getmembers(httpx):
        if inspect.isclass(obj):
            for param in inspect.signature(obj.__init__).parameters.values(): 
                    if str(param.annotation).find('ssl.SSLContext') !=  -1: names.append(f"httpx.{name}")
        elif inspect.isfunction(obj):
            for param in inspect.signature(obj).parameters.values(): 
                if str(param.annotation).find('ssl.SSLContext') !=  -1: names.append(f"httpx.{name}")
    print(", ".join(names[:-1]) + " and " + names[-1])