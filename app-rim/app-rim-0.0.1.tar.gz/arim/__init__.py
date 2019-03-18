name = "arim"

if __name__ == '__main__':
  import layout,sys
  if len(sys.argv) > 0:
    layout.filesOf(sys.argv[1])
