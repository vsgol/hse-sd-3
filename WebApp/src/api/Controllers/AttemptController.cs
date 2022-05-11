using data_lib;
using logic.Data;
using logic.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace api.Controllers;

[Route("api/[controller]")]
[ApiController]
public class AttemptController : Controller
{
    private readonly HwDbContext _context;
    
    public AttemptController(HwDbContext context)
    {
        _context = context;
    }

    public static async void DeleteAttempt(HwDbContext context, Attempt attempt)
    {
        foreach (var comment in context.Comments.Where(c => c.AttemptId == attempt.Id).ToList())
        {
            context.Comments.Remove(comment);
        }

        context.Attempts.Remove(attempt);
        await context.SaveChangesAsync();
    }
    
    // GET: api/Attempt
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Attempt>>> GetAttempts()
    {
        return await _context.Attempts.ToListAsync();
    }
    
    // GET: api/Attempt/1
    [HttpGet("{id}")]
    public async Task<ActionResult<Attempt>> GetAttempt(int id)
    {
        var attempt = await _context.Attempts.FindAsync(id);

        if (attempt == null)
        {
            return NotFound();
        }

        return attempt;
    }
    
    // PUT: api/Attempt/1
    [HttpPut("{id}")]
    public async Task<IActionResult> PutAttempt(int id, Attempt attempt)
    {
        if (id != attempt.Id)
        {
            return BadRequest();
        }

        _context.Entry(attempt).State = EntityState.Modified;

        try
        {
            await _context.SaveChangesAsync();
        }
        catch (DbUpdateConcurrencyException)
        {
            if (!AttemptExists(id))
            {
                return NotFound();
            }
            else
            {
                throw;
            }
        }

        return NoContent();
    }

    // POST: api/Attempt
    [HttpPost]
    public async Task<ActionResult<Attempt>> PostAttempt(Attempt attempt)
    {
        if (!_context.Tasks.Any(e => e.Id == attempt.TaskId))
            return NotFound();
        _context.Attempts.Add(attempt);
        await _context.SaveChangesAsync();
        QueueUtils.SendMessage(attempt.Id.ToString());

        return CreatedAtAction("GetAttempt", new { id = attempt.Id }, attempt);
    }

    // DELETE: api/Attempt/1
    [HttpDelete("{id}")]
    public async Task<ActionResult<Attempt>> DeleteAttempt(int id)
    {
        var attempt = await _context.Attempts.FindAsync(id);
        if (attempt == null)
        {
            return NotFound();
        }

        DeleteAttempt(_context, attempt);
        await _context.SaveChangesAsync();

        return attempt;
    }

    private bool AttemptExists(int id)
    {
        return _context.Attempts.Any(e => e.Id == id);
    }
}