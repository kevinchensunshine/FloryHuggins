from js import document
from pyodide import ffi

log = document.getElementById('values')

def change_value(event):
    log.textContent = event.target.value
    print(event.value)
def main():
  na = document.getElementById("NA")
  na.addEventListener('input', ffi.create_proxy(change_value))
  nb = document.getElementById("NB")
  nb.addEventListener("input", ffi.create_proxy(change_value))
main()