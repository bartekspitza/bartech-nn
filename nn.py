class Tensor:
  def __init__(self, data):
    ## Init with shape
    if isinstance(data, tuple):
      if len(data) > 1:
        raise RuntimeError("Init of shapes with dim > 1 not impl!!!!")
      data = [0] * data[0]

    # Init with actual data
    self.data = data
    self.shape = ()
    curr_dim = data
    while True:
      if isinstance(curr_dim, list):
        curr_dim_len = len(curr_dim)
        self.shape = self.shape + (curr_dim_len, )

        if curr_dim_len > 0:
          curr_dim = curr_dim[0]
        else:
          break
      else:
        break
    self.dim = len(self.shape)
  
  def mult(self, other):
    if not isinstance(other, Tensor):
      raise TypeError("Not Tensor")
    
    # Vector x Vector
    if self.dim == 1 and other.dim == 1:
      if self.shape != other.shape:
        raise RuntimeError(f'Shape {self.shape} does not match {other.shape}')

      new_data = [a*b for a, b in zip(self.data, other.data)]	
      return Tensor(new_data)
    
    # Matrix(dim=2) x Vector
    if self.dim == 1 and other.dim == 2:
      return other.mult(self)
    if self.dim == 2 and other.dim == 1:
      new_data = []
      for d in self.data:
        tmp = Tensor(d)
        res = tmp.mult(other)
        new_data.append(res.data)
      return Tensor(new_data)
  
  def add(self, other):
    if not isinstance(other, Tensor):
      raise TypeError("Not Tensor")
    
    # Vector + Vector
    if self.dim == 1 and other.dim == 1:
      if self.shape != other.shape:
        raise RuntimeError(f'Shape {self.shape} does not match {other.shape}')

      new_data = [a+b for a, b in zip(self.data, other.data)]	
      return Tensor(new_data)
    
    # Matrix(dim=2) + Vector
    if self.dim == 1 and other.dim == 2:
      return other.add(self)
    if self.dim == 2 and other.dim == 1:
      new_data = []
      for d in self.data:
        tmp = Tensor(d)
        res = tmp.add(other)
        new_data.append(res.data)
      return Tensor(new_data)
  
  def sub(self, other):
    if not isinstance(other, Tensor):
      raise TypeError("Not Tensor")
    
    # Vector - Vector
    if self.dim == 1 and other.dim == 1:
      if self.shape != other.shape:
        raise RuntimeError(f'Shape {self.shape} does not match {other.shape}')

      new_data = [a-b for a, b in zip(self.data, other.data)]	
      return Tensor(new_data)
    
    # Matrix(dim=2) + Vector
    if self.dim == 1 and other.dim == 2:
      new_data = []
      for vec in other.data:
        res = [a-b for a, b in zip(self.data, vec)]	
        new_data.append(res)
      return Tensor(new_data)

    if self.dim == 2 and other.dim == 1:
      new_data = []
      for d in self.data:
        tmp = Tensor(d)
        res = tmp.sub(other)
        new_data.append(res.data)
      return Tensor(new_data)
  
  def div(self, other):
    if not isinstance(other, Tensor):
      raise TypeError("Not Tensor")
    
    # Vector - Vector
    if self.dim == 1 and other.dim == 1:
      if self.shape != other.shape:
        raise RuntimeError(f'Shape {self.shape} does not match {other.shape}')

      new_data = [a/b for a, b in zip(self.data, other.data)]	
      return Tensor(new_data)

    # 2d/1d
    if self.dim == 2 and other.dim == 1:
      data = [Tensor(vec).div(other).data for vec in self.data]
      return Tensor(data)

    # 1d/2d
    if self.dim == 1 and other.dim == 2:
      new_data = []
      for vec in other.data:
        res = [a/b for a, b in zip(self.data, vec)]	
        new_data.append(res)
      return Tensor(new_data)
    
  def dot(self, other):
    if not isinstance(other, Tensor):
      raise TypeError("Not Tensor")
    
    if self.dim == 1 and other.dim == 1:
      if self.shape != other.shape:
        raise RuntimeError(f'Shape {self.shape} does not match {other.shape}')

      prod = 0
      for a, b in zip(self.data, other.data):
        prod += a*b
      return prod

    if self.dim == 2 and other.dim == 1:
      new_data = [Tensor(vec).dot(other) for vec in self.data]
      return Tensor(new_data)

    if self.dim == 1 and other.dim == 2:
      if self.shape[0] != other.shape[0]:
        raise RuntimeError(f'Shape {self.shape} does not match {other.shape}')
      
      data = Tensor((other.shape[1], ))
      for i,x in enumerate(self.data):
        intermediate = Tensor([x*w for w in other.data[i]])
        data = data.add(intermediate)
      return data
    
    if (self.dim == 2 and other.dim == 2):
      data = [Tensor(v).dot(other).data for v in self.data]
      return Tensor(data)
  
  def __getitem__(self, indx):
    if not isinstance(indx, int):
      raise RuntimeError("Not implemented")
    return self.data[indx]
  
  def __add__(self, other):
    return self.add(other)

  def __sub__(self, other):
    return self.sub(other)

  def __mul__(self, other):
    return self.mult(other)

  def __truediv__(self, other):
    return self.div(other)
    
  def __matmul__(self, other):
    return self.dot(other)
    
  def __repr__(self):
    return f'Tensor(data={self.data.__repr__()})'

def ones(shape):
  if not isinstance(shape, tuple):
    raise TypeError("Expected tuple")

  dim = len(shape)
  if dim == 0 or dim > 2:
    raise RuntimeError("Invalid size")

  if dim == 1:
    data = [1] * shape[0]
    return Tensor(data)
  if dim == 2:
    data = []
    for row in range(shape[0]):
      data.append([1] * shape[1])
    return Tensor(data)