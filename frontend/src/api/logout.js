let logout = () => {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    window.location.reload(false)
}


export default logout;