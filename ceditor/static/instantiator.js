const {
  CssBaseline,
  ThemeProvider,
  Container,
  InputLabel,
  TextField,
  Button,
  Box,
  Avatar,
  Typography
} = MaterialUI;


function App() {
  const [name, setName] = React.useState("");
  const [created, setCreated] = React.useState(false);
  const inIframe = window.location !== window.parent.location

  React.useEffect(() => {
    if (inIframe) {
      window.parent.postMessage({
        'code': 'initialized',
      }, origin);
    }
  }, [])

  const sendMessage = (code, data) => {
    const dataToSend = {
      id: data._id
    }
    if (inIframe) {
      window.parent.postMessage({
        'code': code,
        'data': dataToSend
      }, origin);
    } else {
      setCreated(dataToSend)
    }
  }

  const submit = () => {
    service.create({ name }).then(response => {
      console.log("RESPONSE CREATE", response.data);
      sendMessage("asset_created", response.data)

    })
  }
  return (
    <Container maxWidth="md">


      {created ?
        (<Box
          sx={{
            maxWidth: 450,
            mx: 'auto',
            alignItems: "center"
          }}
        >
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
            }}
          >
            <Avatar
              src=""
            />
          </Box>
          <Box sx={{ mt: 2 }}>
            <Typography
              align='center'
              color='textPrimary'
              variant='h3'
            >
              Asset created!
            </Typography>
          </Box>
          <Box sx={{ mt: 2 }}>
            <Typography
              align='center'
              color='textSecondary'
              variant='subtitle1'
            >
              The asset is now accessible for this task.
            </Typography>
          </Box>
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              mt: 2,
            }}
          >
            <Button
              color='primary'
              variant='contained'
              href={`${basepath}/assets/${created.id}/view`}
            >
              Open asset
            </Button>
          </Box>
        </Box>)
        : (
          <React.Fragment>
            <InputLabel>Name</InputLabel>

            <TextField error={name === ""} helperText={name === "" && "Required"} variant="outlined" value={name} fullWidth onChange={(e) => setName(e.target.value)} />
            <Button fullWidth variant="contained" sx={{ mt: 2 }} onClick={() => submit()}>Create</Button>
          </React.Fragment>
        )}
    </Container>
  );
}

ReactDOM.render(
  <ThemeProvider theme={theme}>
    {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.querySelector('#root'),
);